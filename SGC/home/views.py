#from django.shortcuts import render

from django.shortcuts import render_to_response
from django.template import RequestContext
from home.forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http import HttpResponseRedirect

def index(request):
    return render_to_response('home/index.html', context_instance = RequestContext(request))

def login(request):
    message = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username,password=password)
                if user is not None and user.is_active:
                    auth_login(request,user)
                    return HttpResponseRedirect('/')
                else:
                    message = "Usuario y/o password incorrecto."
        form = LoginForm()
        ctx = {'form':form, 'message':message}
        return render_to_response('home/login.html', ctx, context_instance=RequestContext(request))
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
