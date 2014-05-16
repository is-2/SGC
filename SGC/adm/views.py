# -*- coding: utf-8 -*-
from django.db.models.query import EmptyQuerySet
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import permission_required, login_required
from adm import forms
from home.models import Client
from adm.models import Project, Phase

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
    """
    Crea un nuevo proyecto.
    """
    form = forms.CreateProjectForm()
    if request.method == "POST":
        form = forms.CreateProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            p = Project(name=name, description=description, state=0)
            p.save()           
            return HttpResponseRedirect('/adm/list_projects/')
        else:
            ctx = {'form':form}
            return render_to_response('adm/project/create_project.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('adm/project/create_project.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def manage_project_phases(request, id_project):
    """
    Despliega las fases que tiene el proyecto seleccionado.
    """
    project = Project.objects.get(id=id_project)    
    phases = Phase.objects.filter(project_id=id_project)
    ctx = {'project':project, 'phases':phases}
    return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def create_project_phase(request, id_project):
    """
    Crea un nueva fase para el proyecto.
    """
    project = Project.objects.get(id=id_project)
    form = forms.CreatePhaseForm()
    
    if request.method == 'POST':
        
        form = forms.CreatePhaseForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            order = form.cleaned_data['order']          
            phase = Phase.objects.create(name=name, state=0, order=order, project=project)
            phase.save()
            ctx = {'project':project, 'phases': Phase.objects.filter(project_id=id_project)}            
            return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))
        
        else:
            ctx = {'form':form, 'project':project}
            return render_to_response('adm/project/create_project_phase.html', ctx, context_instance=RequestContext(request))
        
    ctx = {'form':form, 'project':project}
    return render_to_response('adm/project/create_project_phase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def modify_project_phase(request, id_project, id_phase):
    """
    Modifica una fase.
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    
    if request.method == "POST":
        form = forms.ModifyPhaseForm(data=request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            order = form.cleaned_data['order']
            phase.name = name
            phase.order = order
            phase.save()
            
            ctx = {'project':project, 'phases': Phase.objects.filter(project_id=id_project)}            
            return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))
            
    if request.method == "GET":
        form = forms.ModifyPhaseForm(initial={
            'name' : phase.name,
            'state': phase.state,
            'order': phase.order,            
            })
    ctx = {'form': form, 'project':project, 'phase': phase}
    return render_to_response('adm/project/modify_project_phase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def visualize_phase(request,id_project, id_phase):
    """
    """
    project = Project.objects.get(id=id_project)
    p = Phase.objects.get(id=id_phase)
    ctx = {'project':project, 'phase': p}
    return render_to_response('adm/project/visualize_phase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_project_phase(request, id_project, id_phase):
    """
    Elimina una fase.
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    
    if request.method == "POST":
        phase.delete()
        ctx = {'project':project, 'phases': Phase.objects.filter(project_id=id_project)}          
        return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))
    
    if request.method == "GET":
        ctx = {'project':project, 'phases': Phase.objects.filter(project_id=id_project)}
        return render_to_response('adm/project/delete_project_phase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def manage_project_users(request, id_project):
    """
    Despliega la lista de todos los usuarios del sistema,
    y junto con ellos las opciones de asignar o quitar un
    usuario al proyecto.
    """
    project = Project.objects.get(id=id_project)
    users = User.objects.all()
    ctx = {'project':project, 'users':users}
    return render_to_response('adm/project/manage_project_users.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def assign_project_user(request, id_user, id_project):
    """
    Asigna un usuario al proyecto.
    """
    
    project = Project.objects.get(id=id_project) 
    user = User.objects.get(id=id_user)          
    new_user = False
    
    try:
        user = project.users.get(id=id_user)
    except User.DoesNotExist:
        new_user = True
        
    if new_user:
        project.users.add(user)
        project.save()
    ctx = { 'user':user, 'project':project, 'valid':new_user}
    return render_to_response('adm/project/assign_project_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def remove_project_user(request, id_user, id_project):
    """
    Quita un usuario del proyecto.
    """
    user = User.objects.get(id=id_user)
    project = Project.objects.get(id=id_project)    
    project.users.remove(user)
    project.save()
    
    ctx = { 'user':user, 'project':project}
    return render_to_response('adm/project/remove_project_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def manage_project_committee(request, id_project):
    """
    Despliega la lista de usuarios relacionados con el proyecto,
    junto con las opciones de asignar o quitar un usuario del
    comité de gestión de cambio.
    """
    project = Project.objects.get(id=id_project)    
    users = project.users.all()
    ctx = {'users':users, 'project':project}
    return render_to_response('adm/project/manage_project_committee.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def assign_committee_user(request, id_project, id_user):
    """
    Asigna un usuario al comité de gestión de cambio.
    """
    project = Project.objects.get(id=id_project) 
    user = User.objects.get(id=id_user)          
    new_user = False
    
    try:
        user = project.committee.get(id=id_user)
    except User.DoesNotExist:
        new_user = True
        
    if new_user:
        project.committee.add(user)
        project.save()
    ctx = {'project':project, 'user':user, 'valid':new_user}
    return render_to_response('adm/project/assign_committee_user.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def remove_committee_user(request, id_project, id_user):
    """
    Quita un usuario del comité  de cambio.
    """
    project = Project.objects.get(id=id_project)
    user = User.objects.get(id=id_user)    
    project.committee.remove(user)
    project.save()
    
    ctx = {'project':project, 'user':user}
    return render_to_response('adm/project/remove_committee_user.html', ctx, context_instance=RequestContext(request))

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
def modify_project_state(request, id_project):
    """
    """    
    project = Project.objects.get(id=id_project)
    
    if request.method == "POST":
                
        form = forms.ModifyProjectStateForm(data=request.POST)
                
        if form.is_valid():            
            state = form.cleaned_data['state']
            validOrder = True
                        
            if state=="1":                
                               
                phases = Phase.objects.filter(project_id=id_project)
                project = Project.objects.get(id=id_project)                                   
                for i in range(1, (len(phases)+1)):                                                                                   
                    if not Phase.objects.filter(project=project, order=i):
                        validOrder = False
                        break
                    
            if validOrder:
                project.state = state
                project.save()
                return HttpResponseRedirect('/adm/list_projects/')
            
    if request.method == "GET":
        form = forms.ModifyProjectStateForm(initial={
            'state': project.state,
            })
    ctx = {'form': form, 'project': project}
    return render_to_response('adm/project/modify_project_state.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def modify_phase_state(request, id_project, id_phase):
    """
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    
    if request.method == "POST":
        form = forms.ModifyPhaseStateForm(data=request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            phase.state = state
            phase.save()
            phases = Phase.objects.filter(project_id=id_project)
            ctx = {'project':project, 'phases':phases}
            return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))            
            
    if request.method == "GET":
        form = forms.ModifyPhaseStateForm(initial={
            'state': phase.state,
            })
    ctx = {'form': form, 'project': project, 'phase':phase}
    return render_to_response('adm/project/modify_phase_state.html', ctx, context_instance=RequestContext(request))
    
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

@login_required(login_url='/login/')
def visualize_project(request, id_project):
    """
    """
    project = Project.objects.get(id=id_project)
    ctx = {'project':project}
    return render_to_response('adm/project/visualize_project.html', ctx, context_instance=RequestContext(request))
    