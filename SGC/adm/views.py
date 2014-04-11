#from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from adm.forms import addUserForm
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
    # FIX-HERE?: form = addUserForm(request.POST)
    if request.method == "POST": # POST
        form = addUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phonenum = form.cleaned_data['phonenum']
            direction = form.cleaned_data['direction']
            observation = form.cleaned_data['observation']
            u = User.objects.create_user(username=username, email=email, password=password, 
                                         direction=direction, observation=observation, status=True)
            u.save() # Save information
            return HttpResponseRedirect('/admin/list_users.html')
        else:
            ctx = {'form':form}
            return render_to_response('adm/addUser.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('adm/addUser.html', ctx, context_instance=RequestContext(request))

