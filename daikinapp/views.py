from django.shortcuts import render, redirect
from .forms import *
from django.db import connection
from django.contrib import messages
from datetime import *
from django.core.mail import send_mail

def home_page(request):
    return render(request, 'home.html', {})


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
db = {'1' : 'customerinfo', '2' : 'dealerinfo', '3' : 'seinfo', '4' : 'analystinfo', '5':'expertinfo'}
error_code = {'1' : 'Filter', '2' : 'Compressor', '3': 'Remote', '4': 'Fan', '5': 'Body'}
timeslot = {1: '8 am-10 am', 2: '10 am-12 pm', 3: '12 pm-2 pm', 4: '2 pm-4 pm', 5: '4 pm-6 pm'}
def enter(request):
    userid = "nothing"
    if request.method == "POST":
        userid = request.POST.get('input_text')
        stake = request.POST.get('stakeholder')
        request.session['userid'] = userid
        request.session['stake'] = stake
        if stake is None:
            messages.error(request, 'Please enter stakeholder')
            return redirect('/')
        with connection.cursor() as cursor:
            cursor.execute("select * from " + db[stake] + " where id = %s", [userid])
            results = dictfetchall(cursor)
        if not results:
            messages.error(request, 'Your user id is not correct')
            return redirect('/')
        else:
            name = results[0]['fullname']
            request.session['name'] = name
        if stake == '1':
            return render(request, 'chome.html', {"userid" : userid, "type": stake, "name": name})
        elif stake == '3':
            return render(request, 'sehome.html', {"userid" : userid, "type": stake, "name": name})

def system(request):
    print(request.session['userid'])
    with connection.cursor() as cursor:
        cursor.execute("select system, purchasedate, dealerid from customerinfo where id = %s", [request.session['userid']])
        results = dictfetchall(cursor)
        for item in results:
            purchase = item['purchasedate']
            if (date.today() - purchase).days > 3324:
                item['warranty'] = 'No'
            else:
                item['warranty'] = 'Yes'
        return render(request, 'system.html', {"system" : results})

def senotif(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from notifications where receiverid = %s", [request.session['userid']])
        results = dictfetchall(cursor)
    for item in results:
        temp = item['description']
        item['description'] = error_code[temp]
        temp = item['timeslot']
        item['timeslot'] = timeslot[temp]
        with connection.cursor() as cursor:
            cursor.execute("select system, address from customerinfo where id  = %s", [item['senderid']])
            addr = dictfetchall(cursor)[0]['address']
        item['addr'] = addr
    return render(request, 'senotif.html', {"notifications" : results})

def acceptance(request):
    print('here')
    send_mail(
        'Request accepted',
        'SE has accepted your request',
        'ankansardarndp@gmail.com',
        ['ankansardarth@gmail.com'],
        )
    return render(request, 'senotif.html', {})
