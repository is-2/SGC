#from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from adm.forms import add_user_form, mod_user_form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url = '/login/')
def list_users_view(request):
    """
    Lista todos los usuarios almacenados en el sistema.
    Otorga las opciones de eliminar y modificar a usuario listado.
    """
    users = User.objects.all()
    ctx = {'users':users}
    return render_to_response('users/list_users.html', ctx, content_instance=RequestContext(request))

@login_required(login_url = '/login/')
def add_user_view(request):
    """
    Crea un usuario y lo almacena en el sistema.
    """
    # FIX-HERE?: form = add_user_form(request.POST)
    if request.method == "POST": # POST
        form = add_user_form(request.POST)
        if form.is_valid():
            username    = form.cleaned_data['username']
            password    = form.cleaned_data['password']
            firstName   = form.cleaned_data['firstName']
            lastName    = form.cleaned_data['lastName']
            email       = form.cleaned_data['email']
            phonenum    = form.cleaned_data['phonenum']
            address   = form.cleaned_data['address']
            observation = form.cleaned_data['observation']
            u = User.objects.create_user(username=username, firstName=firstName, lastName=lastName, email=email, password=password, phonenum=phonenum,
                                         address=address, observation=observation, status=True)
            u.save() # Save information
            return HttpResponseRedirect('/admin/list_users.html')
        else:
            ctx = {'form':form}
            return render_to_response('adm/list_users.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('adm/list_users.html', ctx, context_instance=RequestContext(request))

@login_required(login_url = '/login/')
def mod_user_view(request, id_usuario):
    """
    Modifica un usuario existente en el sistema.
    """
    u = User.objects.get(id=id_usuario)
    if request.method == "POST":
        form = mod_user_form(data=request.POST)
        if form.is_valid():
            username    = form.cleaned_data['username']
            password    = form.cleaned_data['password']
            firstName   = form.cleaned_data['firstName']
            lastName    = form.cleaned_data['lastName']
            email       = form.cleaned_data['email']
            phonenum    = form.cleaned_data['phonenum']
            address     = form.cleaned_data['address']
            observation = form.cleaned_data['observation']
            
            u.username  = username
            u.set_password(password)
            u.firstName = firstName
            u.lastName  = lastName
            u.email     = email
            u.phonenum  = phonenum
            u.address   = address
            u.save()
            return HttpResponseRedirect('/admin/list_users.html'%u.id)
            
    if request.method == "GET":
        form = mod_user_form(initial={
            'username' : u.username,            
            'firstName': u.firstName,
            'lastName': u.lastName,
            'email': u.email,
            'phonenum': u.phonenum,
            'address': u.address,
            'observation' : u.observation
            })
    ctx = {'form': form, 'usuario': u}
    return render_to_response('usuario/modificar_usuario.html', ctx, context_instance=RequestContext(request))


