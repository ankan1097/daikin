from django.shortcuts import render, redirect
from .forms import *
from django.db import connection
from django.contrib import messages
from datetime import *

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
