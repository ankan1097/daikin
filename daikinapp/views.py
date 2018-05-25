from django.shortcuts import render
from .forms import *

def home_page(request):
    form = UserForm()
    return render(request, 'home.html', {'form':form})

def enter(request):
    userid = "nothing"
    if request.method == "POST":
        userid = request.POST.get('input_text')
        s = request.POST.get('stakeholder')
    return render(request, 'loggedin.html', {"userid" : userid, "type": s})
