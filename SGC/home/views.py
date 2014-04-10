#from django.shortcuts import render

# Custom imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from adm.models import producto
from home.forms import ContactForm, LoginForm
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http import HttpResponseRedirect
# Create your views here.

# We need to create views using render for simplicity
# def index_view(request):
#    return blablabla

# Custom views (not the best way to do btw)
def index(request):
    return render_to_response('home/index.html', context_instance = RequestContext(request))

def about(request):
    message = "Esto es un mensaje desde mi vista"
    ctx = {'msg':message}
    return render_to_response('home/about.html', ctx, context_instance = RequestContext(request))

def products(request):
    prod = producto.objects.filter(status=True)
    ctx = {'products':prod}
    return render_to_response('home/products.html', ctx, context_instance=RequestContext(request))

def contact(request):
    sent_info = False # Define if the info was sent
    email = ""
    title = ""
    text = ""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            sent_info = True
            email = form.cleaned_data['Email']
            title = form.cleaned_data['Title']
            text = form.cleaned_data['Text']
            
            # Configuracion enviando mensajes
            to_admin = 'akirashimosoeda@gmail.com'
            html_content = "Informacion recibida <br><br><br>***Mensaje***<br><br>%s"%(text)
            msg = EmailMultiAlternatives('Correo de Contacto', html_content, 'from@server.com',[to_admin])
            msg.attach_alternative(html_content,'text/html') # Definimos como contenido html
            msg.send() # Enviamos en correo
            
    else:
        form = ContactForm()
    ctx = {'form':form, 'email':email, 'title':title, 'text':text, 'sent_info':sent_info}
    return render_to_response('home/contact.html', ctx, context_instance=RequestContext(request))

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