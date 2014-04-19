from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from adm.forms import add_user_form, mod_user_form, add_role_form, mod_role_form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from adm.models import Permission, Role


@login_required(login_url = '/login/')
def list_users_view(request):
    """
    Lista todos los usuarios almacenados en el sistema.
    Otorga las opciones de eliminar y modificar a usuario listado.
    """
    users = User.objects.all()
    ctx = {'users':users}
    return render_to_response('adm/list_users.html', ctx, context_instance=RequestContext(request))

@login_required(login_url = '/login/')
def add_user_view(request):
    """
    Crea un usuario y lo almacena en el sistema.
    """
    form = add_user_form()
    if request.method == "POST":
        form = add_user_form(request.POST)
        if form.is_valid():
            username    = form.cleaned_data['username']
            password    = form.cleaned_data['password']
            firstName   = form.cleaned_data['firstName']
            lastName    = form.cleaned_data['lastName']
            email       = form.cleaned_data['email']
            phonenum    = form.cleaned_data['phonenum']
            address     = form.cleaned_data['address']
            observation = form.cleaned_data['observation']
            u = User.objects.create_user(username=username, firstName=firstName, lastName=lastName, email=email, password=password, phonenum=phonenum,
                                         address=address, observation=observation, status=True)
            u.save() # Save information
            return HttpResponseRedirect('/adm/list_users/')
        else:
            ctx = {'form':form}
            return render_to_response('adm/add_user.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('adm/add_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url = '/login/')
def mod_user_view(request, id_user):
    """
    Modifica un usuario.
    """
    u = User.objects.get(id=id_user)
    if request.method == "POST":
        form = mod_user_form(data=request.POST)
        if form.is_valid():
            #username    = form.cleaned_data['username']
            passwd    = form.cleaned_data['passwd']
            firstName   = form.cleaned_data['firstName']
            lastName    = form.cleaned_data['lastName']
            email       = form.cleaned_data['email']
            phonenum    = form.cleaned_data['phonenum']
            address     = form.cleaned_data['address']
            observation = form.cleaned_data['observation']
            
            #u.username  = username
            u.set_password(passwd)
            u.firstName = firstName
            u.lastName  = lastName
            u.email     = email
            u.phonenum  = phonenum
            u.address   = address
            u.observation = observation
            u.save()
            return HttpResponseRedirect('/adm/list_users/')
            
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
    ctx = {'form': form, 'user': u}
    return render_to_response('adm/mod_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url = '/login/')
def del_user_view(request, id_user):
    """
    Elimina un usuario.
    """
    u = User.objects.get(id=id_user)
    if request.method == "POST":
        User.objects.get(id=id_user).delete()
        return HttpResponseRedirect('/adm/list_users/')
    if request.method == "GET":
        ctx = {'user':u}
        return render_to_response('adm/del_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def visualize_user_view(request, id_user):
    """
    Despliega los campos de un usuario.
    """
    u = User.objects.get(id=id_user)
    ctx = {'user': u}
    return render_to_response('adm/visualize_user.html', ctx, context_instance=RequestContext(request))



@login_required(login_url='/login/')
def all_roles_view(request):
    """
    Despliega una lista de todos los roles disponibles del sistema.
    """
    roles = Role.objects.all()
    ctx = {'roles': roles}
    return render_to_response('adm/all_roles.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_role_view(request):
    """
    Agrega un nuevo rol en el sistema.
    """
    form = add_role_form()
    if request.method == "POST":
        form = add_role_form(request.POST)
        if form.is_valid():
            name        = form.cleaned_data['name']
            description = form.cleaned_data['description']
            role = Role.objects.create(name=name, description=description)
            role.save()
            return HttpResponseRedirect('/adm/list_roles/')
        else:
            ctx = {'form':form}
            return render_to_response('adm/add_role.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('adm/add_role.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
# NO OLVIDAR DE ARREGLAR LA DIRECCION
def mod_role_view(request, id_role):
    """
    Modifica un rol del sistema.
    """
    role = Role.objects.get(id=id_role)
    if request.method == "POST":
        form = mod_role_form(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            role.name = name
            role.description = description
            role.save()
            return HttpResponseRedirect('/administracion/gestion_roles/rol/%s'%role.id)
            
    if request.method == "GET":
        form = mod_role_form(initial={
            'name': role.name,
            'description': role.descripction,
            })
    ctx = {'form': form, 'role': role}
    return render_to_response('adm/mod_role.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def del_role_view(request, id_role):
    """
    Elimina un rol del sistema.
    """
    role = Role.objects.get(id=id_role)
    if request.method == "POST":
        Role.objects.get(id=id_role).delete()
        return HttpResponseRedirect('/adm/list_roles/')
    if request.method == "GET":
        ctx = {'role':role}
        return render_to_response('rol/del_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def visualize_role_view(request, id_role):
    """
    Despliega los datos de un rol del sistema.
    """
    role = Role.objects.get(id=id_role)
    ctx = {'role': role}
    return render_to_response('adm/visualize_role.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def user_role_view(request, id_user):
    """
    Lista los roles asignados a un usuario en particular.
    """
    user = User.objects.get(id=id_user)
    roles = Role.objects.filter(user__id=id_user)
    ctx = {'user':user, 'roles':roles}
    return render_to_response('adm/user_role.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def list_role_view(request, id_user):
    """
    Despliega los roles disponibles en el sistema para el usuario seleccionado.
    """
    user = User.objects.get(id=id_user)
    roles = Role.objects.all()
    ctx = {'user':user, 'roles':roles}
    return render_to_response('adm/list_role.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def grant_role_view(request, id_user, id_role):
    """
    Asigna un rol al usuario previamente seleccionado.
    """
    user = User.objects.get(id=id_user)
    role = Role.objects.get(id=id_role)
    new_role = False
    try:
        role = user.roles.get(id=id_role)
    except Role.DoesNotExist:
        new_role = True
    if new_role:
        user.roles.add(role)
        user.save()
    ctx = {'user':user, 'role':role, 'valid':new_role}
    return render_to_response('adm/grant_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def deny_role_view(request, id_user, id_role):
    """
    Quitar un rol al usuario previamente seleccionado.
    """
    user = User.objects.get(id=id_user)
    role = Role.objects.get(id=id_role)
    user.roles.remove(role)
    user.save()
    ctx = {'user':user, 'role':role}
    return render_to_response('user/deny_rol.html', ctx, context_instance=RequestContext(request))



@login_required(login_url='/login/')
def role_permission_view(request, id_role):
    """
    Despliega los permisos con los que cuenta un rol.
    """
    role = Role.objects.get(id=id_role)
    permission = Permission.objects.filter(rol__id=id_role)
    ctx = {'role':role, 'permission':permission}
    return render_to_response('adm/role_permission.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def list_permission_view(request, id_role):
    """
    Despliega los permisos disponibles en el sistema para el rol seleccionado.
    """
    role = Role.objects.get(id=id_role)
    permission = Permission.objects.all()
    ctx = {'role':role, 'permission':permission}
    return render_to_response('adm/list_permission.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def grant_permission_view(request, id_role, id_permission):
    """
    Asigna un permiso al rol previamente seleccionado.
    """    
    role = Role.objects.get(id=id_role)
    permission = Permission.objects.get(id=id_permission)
    new_permission = False
    try:
        permission = role.permissions.get(id=id_permission)
    except Permission.DoesNotExist:
        new_permission = True      
    if new_permission:
        role.permissions.add(permission)
        role.save()
    ctx = {'role':role, 'permission':permission, 'valid':new_permission}
    return render_to_response('adm/grant_permission.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def deny_permission_view(request, id_role, id_permission):
    """
    Quita un permiso del rol previamente seleccionado.    
    """
    role = Role.objects.get(id=id_role)
    permission = Permission.objects.get(id=id_permission)
    role.permisos.remove(permission)
    role.save()
    ctx = {'role':role, 'permission':permission}
    return render_to_response('adm/deny_permission.html', ctx, context_instance=RequestContext(request))
