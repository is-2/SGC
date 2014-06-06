from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from home.forms import LoginForm, SignUpForm
from home.models import Client

# Create your views here.
def index(request):
    """
    Pagina principal.
    """
    if request.user.is_authenticated(): # If user is authenticated.
        count = request.user.mod_requests_committee.all().count()
        ctx = {'count':count}
        return render(request, 'index.html', ctx)
    return render(request, 'index.html')

def sign_up(request):
    """
    Registrar-se.
    """
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username    = form.cleaned_data['username']
            password    = form.cleaned_data['password']
            email       = form.cleaned_data['email']
            telephone   = form.cleaned_data['telephone']
            u = User(username=username, email=email)
            u.set_password(password)
            u.save() # Save information
            u.client = Client(telephone=telephone)
            u.client.save()
            return HttpResponseRedirect('/')
        else:
            ctx = {'form':form}
            return render_to_response('home/signup.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('home/signup.html', ctx, context_instance=RequestContext(request))
    
def log_in(request):
    """
    Login.
    """
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
                    login(request,user)
                    return HttpResponseRedirect('/')
                else:
                    message = "Usuario y/o password incorrecto."
        form = LoginForm()
        ctx = {'form':form, 'message':message}
        return render_to_response('home/login.html', ctx, context_instance=RequestContext(request))
    
def log_out(request):
    """
    Logout.
    """
    logout(request)
    return HttpResponseRedirect('/')

def access_denied(request):
    """
    Funcion que visualiza un mensaje de error por falta de permisos.
    """
        
    if request.method == "GET":
        return render(request, 'home/access_denied.html')