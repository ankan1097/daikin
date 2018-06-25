from django.shortcuts import render, redirect, render_to_response
from .forms import *
from django.db import connection
from django.contrib import messages
from datetime import *
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
import json
from django.template import RequestContext

def home_page(request):
	return render(request, 'home.html', {})


def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]
db = {1 : 'customerinfo', 2 : 'dealerinfo', 3 : 'seinfo', 4 : 'analystinfo', 5:'expertinfo'}
typ = {1 : 'Customer', 2 : 'Dealer', 3 : 'Service Engineer', 4 : 'Analyst', 5 : 'Expert'}
error_code = {'0' : 'Accepted', '1' : 'Filter', '2' : 'Compressor', '3': 'Remote', '4': 'Fan', '5': 'Body'}
timeslot = {1: '8 am-10 am', 2: '10 am-12 pm', 3: '12 pm-2 pm', 4: '2 pm-4 pm', 5: '4 pm-6 pm'}
def enter(request):
	userid = "nothing"
	results = list()
	stake = 1
	if request.method == "POST":
		userid = request.POST.get('input_text')
		pw = request.POST.get('input_pass')
		request.session['userid'] = userid
		if pw is None:
			messages.error(request, 'Please enter stakeholder')
			return redirect('/')
		with connection.cursor() as cursor:
			for stake in range(1,6):	
				cursor.execute("select * from " + db[stake] + " where id = %s and password = %s", [userid, pw])
				results = dictfetchall(cursor)
				if results:
					break
			if not results:
				messages.error(request, 'Your user id or password is not correct')
				return redirect('/')
			else:
				if stake == 1 or stake == 2:
					name = results[0]['fullname']
					email = results[0]['email']
					addr = results[0]['address']
					request.session['name'] = name
				elif stake == 3:
					name = results[0]['fullname']
					email = results[0]['email']
					rating = results[0]['rating']
					skill = results[0]['skilllevel']
					request.session['name'] = name
				elif stake == 4:
					name = results[0]['fullname']
					email = results[0]['email']
					request.session['name'] = name
	###################  For number of notifications ##################################
		with connection.cursor() as cursor:
			cursor.execute('select count(id) from notifications where read = %s and receiverid = %s',[False, userid])
			count = dictfetchall(cursor)
	###################  For notifications #############################################
		with connection.cursor() as cursor:
			cursor.execute("select * from notifications where receiverid = %s order by id desc", [userid])
			results = dictfetchall(cursor)
		for item in results:
			temp = item['description']
			item['description'] = error_code[temp]
			temp = item['timeslot']
			item['timeslot'] = timeslot[temp]
			if item['day'] <= datetime.today().date():
				item['invalid'] = True
			if stake == '3':
				with connection.cursor() as cursor:
					cursor.execute("select address from customerinfo where id  = %s", [item['senderid']])
					addr = dictfetchall(cursor)[0]['address']
				item['addr'] = addr
			with connection.cursor() as cursor:
				cursor.execute("update notifications set read = True where read = False and receiverid = %s", [request.session['userid']])
	#################### Returning #######################################################
		if stake == 1:
			return render(request, 'chome.html', {"userid" : userid, "type": stake, "name": name, "email": email, "address": addr, 
				"type": typ[stake], "count": count[0]['count'], "notifications" : results})
		elif stake == 2: 
			with connection.cursor() as cursor:
				cursor.execute('select * from components where ownerid = %s', [request.session['userid']])
				comps = dictfetchall(cursor)
			return render(request, 'dhome.html', {"userid" : userid, "type": stake, "name": name, "email": email, "address": addr, 
				"count": count[0]['count'], "components" : comps, "notifications" : results})
		elif stake == 3:
			with connection.cursor() as cursor:
				cursor.execute('select * from components where ownerid = %s', [request.session['userid']])
				comps = dictfetchall(cursor)
			return render(request, 'sehome.html', {"userid" : userid, "type": stake, "name": name, "email": email, "skill": skill, "rating": rating, "count": count[0]['count'],
			 "components" : comps, "notifications" : results})

		elif stake == 4:
			return render(request, 'analhome.html', {"userid": userid, "type": stake, "name": name, "email": email})

################################ Showing the system lists for the customer #########################
def system(request):
	with connection.cursor() as cursor:
		cursor.execute("select modelid, purchasedate, dealerid from outdoorunit where ownerid = %s", [request.session['userid']])
		results = dictfetchall(cursor)
		for item in results:
			cursor.execute("select modelid from indoorunit where outdoorid = %s", [item['modelid']])
			indoors = dictfetchall(cursor)
			item['indoors'] = indoors
			purchase = item['purchasedate']
			if (date.today() - purchase).days > 3324:
				item['warranty'] = 'No'
			else:
				item['warranty'] = 'Yes'
	return render(request, 'system.html', {"system" : results})

############################## Notitification details of a notification ###########################
def senotif(request):
	if request.method == 'GET':
		notif = request.GET.get('notif_id')
	with connection.cursor() as cursor:
		cursor.execute("select * from notifications where id = %s", [notif])
		results = dictfetchall(cursor)
	for item in results:
		temp = item['description']
		item['description'] = error_code[temp]
		temp = item['timeslot']
		item['timeslot'] = timeslot[temp]
		if item['day'] <= datetime.today().date():
			item['invalid'] = True
		with connection.cursor() as cursor:
			cursor.execute("select system, address from customerinfo where id  = %s", [item['senderid']])
			info = dictfetchall(cursor)
		item['addr'] = info[0]['address']
		item['model'] = info[0]['system']
	return render(request, 'senotif.html', {"notification": results[0]})
	# return HttpResponse(response)

def cnotif(request):
	with connection.cursor() as cursor:
		cursor.execute("select * from notifications where receiverid = %s order by id desc", [request.session['userid']])
		results = dictfetchall(cursor)
	for item in results:
		temp = item['timeslot']
		item['timeslot'] = timeslot[temp]
		if item['day'] <= datetime.today().date():
			item['invalid'] = True
	with connection.cursor() as cursor:
		cursor.execute("update notifications set read = True where read = False")
	return render(request, 'cnotif.html', {"notifications" : results})

####################################### SE Accepting a service request ########################
def acceptance(request):
	if request.method == 'GET':
		notif = request.GET.get('notif_id')
	with connection.cursor() as cursor:
		cursor.execute('select * from notifications where id = %s', [notif])
		results = dictfetchall(cursor)
		receiverid = results[0]['senderid']
		day = results[0]['day']
		timeslot = results[0]['timeslot']
		cursor.execute("select * from schedule where userid = %s and day = %s and timeslot = %s", [request.session['userid'], day, timeslot])
		results = dictfetchall(cursor)
		if not results:
			cursor.execute("insert into notifications(senderid, receiverid, description, day, read, timeslot) values(%s, %s, %s, %s, %s, %s)", 
				[request.session['userid'], receiverid,'0', day, False, timeslot])
			cursor.execute("select latitude, longitude from customerinfo where id = %s", [receiverid])
			position = dictfetchall(cursor)
			cursor.execute("insert into schedule(userid, day, timeslot, latitude, longitude) values(%s, %s, %s, %s, %s)", [request.session['userid'], day, timeslot, position[0]['latitude'], position[0]['longitude']])
			final = 'success'
		else:
			final = 'failed'
		cursor.execute('update notifications set invalid = %s where id = %s', [True, notif])
	return JsonResponse({'same': final})

################################# SE rejecting a service request ##########################
def rejection(request):
	if request.method == 'GET':
		notif = request.GET.get('notif_id')

################################ Data about customers for dealers #########################
def custdata(request):
	with connection.cursor() as cursor:
		cursor.execute('select * from customerinfo where dealerid = %s', [request.session['userid']])
		results = dictfetchall(cursor)
		for item in results:
			cursor.execute('select modelid, purchasedate from outdoorunit where ownerid = %s and dealerid = %s', 
				[item['id'], request.session['userid']])
			models = dictfetchall(cursor)
			for unit in models:
				cursor.execute('select modelid from indoorunit where outdoorid = %s', [unit['modelid']])
				ins = dictfetchall(cursor)
				unit['indoors'] = ins
			item['outdoors'] = models
	return render(request, 'custdata.html', {'data': results})

##################### For components search ##########################################
def search(request):
	if request.method == 'GET':
		q = request.GET.get('comp')
		with connection.cursor() as cursor:
			cursor.execute("select * from components where compname like '%" + q + "%'")
			results = dictfetchall(cursor)
		for item in results:
			with connection.cursor() as cursor:
				if item['ownerid'][0] == '8':
					cursor.execute("select email from seinfo where id = %s", [item['ownerid']])
					item['type'] = 'Service Engineer'
				else:
					cursor.execute("select email from dealerinfo where id = %s", [item['ownerid']])
					item['type'] = 'Dealer'
				locations = dictfetchall(cursor)
				item['mail'] = locations[0]['email']

	return render(request, 'secomp.html', {'components': results, 'string': q})


############################# Loading the map data #######################################

def mapdata(request):
	markers = dict()
	if request.method == 'GET':
		with connection.cursor() as cursor:
			cursor.execute("select id, fullname, email, latitude, longitude, address from customerinfo;")
			results = dictfetchall(cursor)
			markers['customers'] = results
			cursor.execute("select id, fullname, email, latitude, longitude, skilllevel, rating from seinfo;")
			results = dictfetchall(cursor)
			markers['se'] = results
			cursor.execute("select id, fullname, email, latitude, longitude, address from dealerinfo;")
			results = dictfetchall(cursor)
			markers['dealers'] = results
			cursor.execute("select id, fullname, email, latitude, longitude from analystinfo;")
			results = dictfetchall(cursor)
			markers['analyst'] = results
			cursor.execute("select id, fullname, email, latitude, longitude from expertinfo;")
			results = dictfetchall(cursor)
			markers['experts'] = results
	return JsonResponse(markers)


########################## Dealer's system details viewing ##########################

def dsystem(request):
	if request.method == 'GET':
		q = request.GET.get('user')
	with connection.cursor() as cursor:
		cursor.execute("select modelid, purchasedate, dealerid from outdoorunit where ownerid = %s", [q])
		results = dictfetchall(cursor)
		for item in results:
			cursor.execute("select modelid from indoorunit where outdoorid = %s", [item['modelid']])
			indoors = dictfetchall(cursor)
			item['indoors'] = indoors
			purchase = item['purchasedate']
			if (date.today() - purchase).days > 3324:
				item['warranty'] = 'No'
			else:
				item['warranty'] = 'Yes'
	return render(request, 'system.html', {"system" : results})

################################## Starting the chatbox #################################
def chatstart(request):
	return render(request, 'chat.html', {'name': request.session['name']})

############################### Chat sending ###############################################

receiverid = 'nothing'
def chat(request):
	global receiverid
	user1 = request.session['userid']
	results = list()
	if request.method == 'GET':
		message = request.GET.get('msg')
		time = request.GET.get('time')
	print(message, time)
	if "chat@" in message:
		receiverid = message[5:]
		print("receiverid", receiverid)
		request.session[user1] = receiverid
	else:
		if receiverid == 'nothing':
			#do something
			print('here')
		else:
			with connection.cursor() as cursor:
				cursor.execute('insert into messages values(default, %s, %s, %s, %s, %s)',
				 [user1, receiverid, message, False, time])
	return render(request, 'message.html', {})

############################# Chat receiving ##############################################

def chatrefresh(request):
	with connection.cursor() as cursor:
		cursor.execute('select senderid, message, timestamp from messages where receiverid = %s and seen = false',
		 [request.session['userid']])
		results = dictfetchall(cursor)
		if not results:
			new = False
		else:
			new = True
			cursor.execute('update messages set seen = true where receiverid = %s', [request.session['userid']])
	return render(request, 'message.html', {'message': results, 'new': new})


def feedback(request):
	return render(request, 'feedback.html', {})

################################## Showing real time data ######################################
offset = -1
def realtime(request):
	global offset
	offset += 1
	with connection.cursor() as cursor:
		if offset % 2 == 0:
			cursor.execute("select ta, tb, tf, ti, tsc, tsh, hp, lp, inv1, inv2, " + 
				"lo_export(realtimedata.graph, 'C:/Users/c-ankan/Documents/webApp/daikinapp/static/css/PC0.png') " + 
				"from realtimedata limit 1 offset %s", [offset])
		else:
			cursor.execute("select ta, tb, tf, ti, tsc, tsh, hp, lp, inv1, inv2, " + 
				"lo_export(realtimedata.graph, 'C:/Users/c-ankan/Documents/webApp/daikinapp/static/css/PC1.png') " + 
				"from realtimedata limit 1 offset %s", [offset])
		results = dictfetchall(cursor)
		# open('hey.png', 'wb').write(bytes(results[0]['graph']))
		# temp = str(results[0]['graph'])
		# results[0]['graph'] = temp
	return JsonResponse(results[0])
	# return HttpResponse('se')


############################# Reporting the issue ############################################

def report(request):
	if request.method == 'GET':
		v1 = request.GET.get('value1')
		v2 = request.GET.get('value2')
		v3 = request.GET.get('value3')
		v4 = request.GET.get('value4')
		v5 = request.GET.get('value5')
		v6 = request.GET.get('value6')
		v7 = request.GET.get('value7')

	with connection.cursor() as cursor:
		cursor.execute("insert into pendingrequests values(default, ")