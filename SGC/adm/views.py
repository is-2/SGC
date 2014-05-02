from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import permission_required, login_required
from adm import forms
from home.models import Client
from adm.models import Project

# Create your views here.
@login_required(login_url='/login/')
def list_users(request):
    """
    Lista todos los usuarios almacenados en el sistema.
    Otorga las opciones de eliminar y modificar a usuario listado.
    """
    users = User.objects.all()
    ctx = {'users':users}
    return render_to_response('adm/user/list_users.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
def add_user(request):
    """
    Crea un usuario y lo almacena en el sistema.
    """
    form = forms.AddUserForm()
    if request.method == "POST":
        form = forms.AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            address = form.cleaned_data['address']
            observation = form.cleaned_data['observation']
            u = User(username=username, first_name=first_name, last_name=last_name, email=email)
            u.set_password(password)
            u.save()  # Save information
            u.client = Client(telephone=telephone, address=address, observation=observation)
            u.client.save()
            return HttpResponseRedirect('/adm/list_users/')
        else:
            ctx = {'form':form}
            return render_to_response('adm/user/add_user.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('adm/user/add_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def modify_user(request, id_user):
    """
    Modifica un usuario.
    """
    u = User.objects.get(id=id_user)
    if request.method == "POST":
        form = forms.ModUserForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            address = form.cleaned_data['address']
            observation = form.cleaned_data['observation']
            
            u.set_password(password)
            u.first_name = first_name
            u.last_name = last_name
            u.email = email
            u.save()
            u.client.telephone = telephone
            u.client.address = address
            u.client.observation = observation
            u.client.save()
            return HttpResponseRedirect('/adm/list_users/')
            
    if request.method == "GET":
        form = forms.ModUserForm(initial={
            'username' : u.username,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'telephone': u.client.telephone,
            'address': u.client.address,
            'observation' : u.client.observation
            })
    ctx = {'form': form, 'user': u}
    return render_to_response('adm/user/modify_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_user(request, id_user):
    """
    Elimina un usuario.
    """
    u = User.objects.get(id=id_user)
    if request.method == "POST":
        User.objects.get(id=id_user).delete()
        return HttpResponseRedirect('/adm/list_users/')
    if request.method == "GET":
        ctx = {'user':u}
        return render_to_response('adm/user/delete_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def visualize_user(request, id_user):
    """
    Despliega los campos de un usuario.
    """
    u = User.objects.get(id=id_user)
    ctx = {'user': u}
    return render_to_response('adm/user/visualize_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def assign_user_groups(request, id_user):
    """
    
    """
    user = User.objects.get(id=id_user)
    # groups = Group.objects.filter(user__id=id_user)
    groups = Group.objects.all()
    ctx = {'user':user, 'groups':groups}
    return render_to_response('adm/group/assign_user_groups.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
def grant_user_group(request, id_user, id_group):
    """
    """
    u = User.objects.get(id=id_user)
    g = Group.objects.get(id=id_group)
    new_group = False
    try:
        g = u.groups.get(id=id_group)
    except Group.DoesNotExist:
        new_group = True
    if new_group:
        u.groups.add(g)
    ctx = {'user':u, 'group':g, 'valid':new_group}
    return render_to_response('adm/group/grant_user_group.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def deny_user_group(request, id_user, id_group):
    """
    Quitar un rol al usuario previamente seleccionado.
    """
    user = User.objects.get(id=id_user)
    group = Group.objects.get(id=id_group)
    user.groups.remove(group)
    ctx = {'user':user, 'group':group}
    return render_to_response('adm/group/deny_user_group.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def list_groups(request):
    groups = Group.objects.all()
    ctx = {'groups':groups}
    return render_to_response('adm/group/list_groups.html', ctx, context_instance=RequestContext(request))

@permission_required('home.puede_crear_rol', login_url='/login/')
def create_group(request):
    form = forms.CreateGroupForm()
    if request.method == "POST":
        form = forms.CreateGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            g = Group(name=name)
            g.save()  # Save information
            return HttpResponseRedirect('/adm/list_groups/')
        else:
            ctx = {'form':form}
            return render_to_response('adm/group/create_group.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('adm/group/create_group.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def modify_group(request, id_group):
    """
    Modifica un rol del sistema.
    """
    group = Group.objects.get(id=id_group)
    if request.method == "POST":
        form = forms.ModGroupForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            group.name = name
            group.save()
            return HttpResponseRedirect('/adm/list_groups/')
            
    if request.method == "GET":
        form = forms.ModGroupForm(initial={
            'name': group.name,
            })
    ctx = {'form': form, 'group': group}
    return render_to_response('adm/group/modify_group.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_group(request, id_group):
    """
    Elimina un rol del sistema.
    """
    group = Group.objects.get(id=id_group)
    if request.method == "POST":
        # Role.objects.get(id=id_role).delete()
        group.delete()
        return HttpResponseRedirect('/adm/list_groups/')
    if request.method == "GET":
        ctx = {'group':group}
        return render_to_response('adm/group/delete_group.html', ctx, context_instance=RequestContext(request))
    
def assign_permissions(request, id_group):
    group = Group.objects.get(id=id_group)
    perms = Permission.objects.all()
    ctx = {'group':group, 'permissions':perms}
    return render_to_response('adm/perm/assign_perm.html', ctx, context_instance=RequestContext(request))

def grant_permissions(request, id_group, id_perm):
    group = Group.objects.get(id=id_group)
    permission = Permission.objects.get(id=id_perm)
    new_permission = False
    try:
        permission = group.permissions.get(id=id_perm)
    except Permission.DoesNotExist:
        new_permission = True      
    if new_permission:
        group.permissions.add(permission)
        group.save()
    ctx = {'group':group, 'permission':permission, 'valid':new_permission}
    return render_to_response('adm/perm/grant_perm.html', ctx, context_instance=RequestContext(request))

def deny_permissions(request, id_group, id_perm):
    group = Group.objects.get(id=id_group)
    permission = Permission.objects.get(id=id_perm)
    group.permissions.remove(permission)
    group.save()
    ctx = {'group':group, 'permission':permission}
    return render_to_response('adm/perm/deny_perm.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def list_projects(request):
    """
    Listan todos los projectos existentes en el sistema.
    """
    projects = Project.objects.all()
    ctx = {'projects':projects}
    return render_to_response('adm/project/list_projects.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def create_project(request):
    form = forms.CreateProjectForm()
    if request.method == "POST":
        form = forms.CreateProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            g = Project(name=name, description=description)
            g.save()  # Save information
            return HttpResponseRedirect('/adm/list_projects/')
        else:
            ctx = {'form':form}
            return render_to_response('adm/project/create_project.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('adm/project/create_project.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def modify_project(request, id_project):
    """
    Modifica un proyecto del sistema.
    """
    project = Project.objects.get(id=id_project)
    if request.method == "POST":
        form = forms.ModifyProjectForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            project.name = name
            project.description = description
            project.save()
            return HttpResponseRedirect('/adm/list_projects/')
            
    if request.method == "GET":
        form = forms.ModifyProjectForm(initial={
            'name': project.name,
            'description': project.description,
            })
    ctx = {'form': form, 'project': project}
    return render_to_response('adm/project/modify_project.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_project(request, id_project):
    """
    Elimina un proyecto.
    """
    p = Project.objects.get(id=id_project)
    if request.method == "POST":
        Project.objects.get(id=id_project).delete()
        return HttpResponseRedirect('/adm/list_projects/')
    if request.method == "GET":
        ctx = {'project':p}
        return render_to_response('adm/project/delete_project.html', ctx, context_instance=RequestContext(request))
