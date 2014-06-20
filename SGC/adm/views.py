# -*- coding: utf-8 -*-

from itertools import chain
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import permission_required, login_required
from adm import forms
from home.models import Client
from adm.models import Project, Phase
from des.models import Item, BaseLine
from gdc.models import ModificationRequest

# Create your views here.
@permission_required('home.puede_visualizar_usuario', login_url='access_denied')
def list_users(request):
    """
    Lista todos los usuarios almacenados en el sistema.
    Otorga las opciones de eliminar y modificar a usuario listado.
    """
    if request.method == "GET":
        users = User.objects.filter(is_active=True)
        ctx = {'users':users}
        return render(request, 'adm/user/list_users.html', ctx)
    
@permission_required('home.puede_crear_usuario', login_url='access_denied')
def add_user(request):
    """
    Crea un usuario y lo almacena en el sistema.
    """
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
        
    if request.method == "GET":     
        form = forms.AddUserForm()   
        ctx = {'form':form}
        return render_to_response('adm/user/add_user.html', ctx, context_instance=RequestContext(request))

@permission_required('home.puede_modificar_usuario', login_url='access_denied')
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
        else:
            ctx = {'form': form, 'user': u}
            return render_to_response('adm/user/modify_user.html', ctx, context_instance=RequestContext(request))
            
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

@permission_required('home.puede_eliminar_usuario', login_url='access_denied')
def delete_user(request, id_user):
    """
    Elimina un usuario.
    """
    if request.method == "POST":
        user = User.objects.get(id=id_user)
        user.is_active = False
        user.save()
        return redirect(reverse('list_users'))
    
    if request.method == "GET":
        user = User.objects.get(id=id_user)
        ctx = {'user':user}
        return render(request, 'adm/user/delete_user.html', ctx)

@permission_required('home.puede_visualizar_usuario', login_url='access_denied')
def visualize_user(request, id_user):
    """
    Despliega los campos de un usuario.
    """
    u = User.objects.get(id=id_user)
    ctx = {'user': u}
    return render_to_response('adm/user/visualize_user.html', ctx, context_instance=RequestContext(request))

@permission_required('home.puede_asignar_rol', login_url='access_denied')
def assign_user_groups(request, id_user):
    """
    Funcion que asigna un Rol a un Usuario.
    """
    if request.method == "GET":
        user = User.objects.get(id=id_user)
        groups = Group.objects.all()
        ctx = {'user':user, 'groups':groups}
        return render_to_response('adm/group/assign_user_groups.html', ctx, context_instance=RequestContext(request))
    
@permission_required('home.puede_asignar_rol', login_url='access_denied')
def grant_user_group(request, id_user, id_group):
    """
    """
    u = User.objects.get(id=id_user)
    g = Group.objects.get(id=id_group)
    groups = Group.objects.all()
    new_group = False
    try:
        g = u.groups.get(id=id_group)
    except Group.DoesNotExist:
        new_group = True
    if new_group:
        u.groups.add(g)
    ctx = {'user':u, 'groups':groups}
    return render_to_response('adm/group/assign_user_groups.html', ctx, context_instance=RequestContext(request))

@permission_required('home.puede_asignar_rol', login_url='access_denied')
def deny_user_group(request, id_user, id_group):
    """
    Quitar un rol al usuario previamente seleccionado.
    """
    user = User.objects.get(id=id_user)
    group = Group.objects.get(id=id_group)
    groups = Group.objects.all()
    
    user.groups.remove(group)
    ctx = {'user':user, 'groups':groups}
    return render_to_response('adm/group/assign_user_groups.html', ctx, context_instance=RequestContext(request))

@permission_required('home.puede_visualizar_rol', login_url='access_denied')
def list_groups(request):
    groups = Group.objects.all()
    ctx = {'groups':groups}
    return render_to_response('adm/group/list_groups.html', ctx, context_instance=RequestContext(request))

@permission_required('home.puede_crear_rol', login_url='access_denied')
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

@permission_required('home.puede_modificar_rol', login_url='access_denied')
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

@permission_required('home.puede_eliminar_rol', login_url='access_denied')
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

@permission_required('home.puede_asignar_permiso', login_url='access_denied')
def assign_permissions(request, id_group):
    if request.method == "GET":
        group = Group.objects.get(id=id_group)
        perms = Permission.objects.exclude(name__startswith="Can").order_by('id')
        ctx = {'group':group, 'permissions':perms}
        return render(request, 'adm/perm/assign_perm.html', ctx)

@permission_required('home.puede_asignar_permiso', login_url='access_denied')
def grant_permissions(request, id_group, id_perm):
    if request.method == "GET":
        group = Group.objects.get(id=id_group)
        perm = Permission.objects.get(id=id_perm)
        group.permissions.add(perm)
        group.save()
        ctx = {'id_group':id_group}
        return redirect(reverse('assign_perm', kwargs=ctx))

@permission_required('home.puede_asignar_permiso', login_url='access_denied')
def deny_permissions(request, id_group, id_perm):
    if request.method == "GET":
        group = Group.objects.get(id=id_group)
        perm = Permission.objects.get(id=id_perm)
        group.permissions.remove(perm)
        group.save()
        ctx = {'id_group':id_group}
        return redirect(reverse('assign_perm', kwargs=ctx))

@permission_required('adm.puede_visualizar_proyecto', login_url='access_denied')
def list_projects(request):
    """
    Listan todos los projectos existentes en el sistema.
    """
    projects = Project.objects.all()
    ctx = {'projects':projects}
    return render_to_response('adm/project/list_projects.html', ctx, context_instance=RequestContext(request))

@permission_required('adm.puede_crear_proyecto', login_url='access_denied')
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

@permission_required('adm.puede_visualizar_fase', login_url='access_denied')
def manage_project_phases(request, id_project):
    """
    Despliega las fases que tiene el proyecto seleccionado.
    """
    project = Project.objects.get(id=id_project)    
    phases = Phase.objects.filter(project_id=id_project)
    ctx = {'project':project, 'phases':phases}
    return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))

@permission_required('adm.puede_crear_fase', login_url='access_denied')
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
            
            if not Phase.objects.filter(project=project, order=order):                     
                phase = Phase.objects.create(name=name, state=0, order=order, project=project)
                phase.save()
                ctx = {'project':project, 'phases': Phase.objects.filter(project_id=id_project)}            
                return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))        
        else:
            ctx = {'form':form, 'project':project}
            return render_to_response('adm/project/create_project_phase.html', ctx, context_instance=RequestContext(request))
        
    ctx = {'form':form, 'project':project}
    return render_to_response('adm/project/create_project_phase.html', ctx, context_instance=RequestContext(request))

@permission_required('adm.puede_modificar_fase', login_url='access_denied')
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

@permission_required('adm.puede_visualizar_fase', login_url='access_denied')
def visualize_phase(request,id_project, id_phase):
    """
    """
    project = Project.objects.get(id=id_project)
    p = Phase.objects.get(id=id_phase)
    ctx = {'project':project, 'phase': p}
    return render_to_response('adm/project/visualize_phase.html', ctx, context_instance=RequestContext(request))

@permission_required('adm.puede_eliminar_fase', login_url='access_denied')
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

@permission_required('home.puede_asignar_usuario', login_url='access_denied')
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

@permission_required('home.puede_asignar_usuario', login_url='access_denied')
def assign_project_user(request, id_user, id_project):
    """
    Asigna un usuario al proyecto.
    """
    
    project = Project.objects.get(id=id_project) 
    user = User.objects.get(id=id_user)
    users = User.objects.all()          
    new_user = False
    
    try:
        user = project.users.get(id=id_user)
    except User.DoesNotExist:
        new_user = True
        
    if new_user:
        project.users.add(user)
        project.save()
    ctx = {'project':project, 'users':users }
    return render_to_response('adm/project/manage_project_users.html', ctx, context_instance=RequestContext(request))

@permission_required('home.puede_asignar_usuario', login_url='access_denied')
def remove_project_user(request, id_user, id_project):
    """
    Quita un usuario del proyecto.
    """
    user = User.objects.get(id=id_user)
    project = Project.objects.get(id=id_project)
    users = User.objects.all()     
        
    project.users.remove(user)
    project.save()
    
    ctx = {'project':project, 'users':users}
    return render_to_response('adm/project/manage_project_users.html', ctx, context_instance=RequestContext(request))

@permission_required('home.puede_asignar_usuario', login_url='access_denied')
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

@permission_required('home.puede_asignar_usuario', login_url='access_denied')
def assign_committee_user(request, id_project, id_user):
    """
    Asigna un usuario al comité de gestión de cambio.
    """
    project = Project.objects.get(id=id_project) 
    user = User.objects.get(id=id_user)
    users = project.users.all()          
    new_user = False
    
    try:
        user = project.committee.get(id=id_user)
    except User.DoesNotExist:
        new_user = True
        
    if new_user:
        project.committee.add(user)
        project.save()
    ctx = {'project':project, 'users':users}
    return render_to_response('adm/project/manage_project_committee.html', ctx, context_instance=RequestContext(request))

@permission_required('home.puede_asignar_usuario', login_url='access_denied')
def remove_committee_user(request, id_project, id_user):
    """
    Quita un usuario del comité  de cambio.
    """
    project = Project.objects.get(id=id_project)
    user = User.objects.get(id=id_user)
    users = project.users.all()
        
    project.committee.remove(user)
    project.save()
    
    ctx = {'project':project, 'users':users}
    return render_to_response('adm/project/manage_project_committee.html', ctx, context_instance=RequestContext(request))

@permission_required('adm.puede_modificar_proyecto', login_url='access_denied')
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

@permission_required('adm.puede_modificar_proyecto', login_url='access_denied')
def modify_project_state(request, id_project):
    """
    """    
    project = Project.objects.get(id=id_project)
    
    if request.method == "POST":                
        form = forms.ModifyProjectStateForm(data=request.POST)                
        if form.is_valid():            
            state = form.cleaned_data['state']
            
            # ESTADO a PENDIENTE.
            if state == "0":
                for phase in Phase.objects.filter(project=project):
                    phase.state="0"
                    phase.save()    # FASES: INICIAL.
                project.state = state
                project.save()  # PROYECTO: PENDIENTE.
                return HttpResponseRedirect('/adm/list_projects/')
            
            # ESTADO a ACTIVO.                                   
            if state == "1":
                validOrder = True                               
                phases = Phase.objects.filter(project=project)                                  
                for i in range(1, (len(phases)+1)):                                                                                   
                    if not Phase.objects.filter(project=project, order=i):
                        validOrder = False
                        break
                    
                if validOrder:  # ORDEN CORRECTO.
                    for phase in Phase.objects.filter(project=project):
                        phase.state="1"
                        phase.save()    # FASES: DESARROLLO.
                    project.state = state
                    project.save()  # PROYECTO: ACTIVO.
                    return HttpResponseRedirect('/adm/list_projects/')
                
            # ESTADO a FINALIZADO.
            if state == "2":
                phasesFinished = True
                for phase in Phase.objects.filter(project=project):
                    if phase.state != 2:
                        phasesFinished = False
                        break
            
                if phasesFinished:
                    project.state = state
                    project.save()  # PROYECTO: FINALIZADO.
                    return HttpResponseRedirect('/adm/list_projects/')                    
                            
    if request.method == "GET":
        form = forms.ModifyProjectStateForm(initial={
            'state': project.state,
            })
    ctx = {'form': form, 'project': project}
    return render_to_response('adm/project/modify_project_state.html', ctx, context_instance=RequestContext(request))

@permission_required('adm.puede_modificar_fase', login_url='access_denied')
def modify_phase_state(request, id_project, id_phase):
    """
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    
    if request.method == "POST":
        form = forms.ModifyPhaseStateForm(data=request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            
            # ESTADO a INICIAL. **
            if state == "0":
                phase.state = state
                phase.save()    # FASE: INICIAL.
                phases = Phase.objects.filter(project=project)
                ctx = {'project':project, 'phases':phases}
                return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))
            
            # ESTADO a DESARROLLO. **
            if state == "1":
                phase.state = state
                phase.save()    # FASE: DESARROLLO.
                phases = Phase.objects.filter(project=project)
                ctx = {'project':project, 'phases':phases}
                return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))
            
            # ESTADO A FINALIZADO.
            if state == "2": 
                itemsApproved = True
                for item in Item.objects.filter(phase=phase):
                    if item.baseline is None:
                        itemsApproved = False
                        break
                
                baselineClosed = True
                for baseline in BaseLine.objects.filter(phase=phase):
                    if baseline.state != 1:
                        baselineClosed = False
                        break
                
                if itemsApproved and baselineClosed:    # ITEMS APROBADOS Y LB CERRADAS.
                    phase.state = state
                    phase.save()    # FASE: FINALIZADA.
                    phases = Phase.objects.filter(project=project)
                    ctx = {'project':project, 'phases':phases}
                    return render_to_response('adm/project/manage_project_phases.html', ctx, context_instance=RequestContext(request))            
            
    if request.method == "GET":
        form = forms.ModifyPhaseStateForm(initial={
            'state': phase.state,
            })
    ctx = {'form': form, 'project': project, 'phase':phase}
    return render_to_response('adm/project/modify_phase_state.html', ctx, context_instance=RequestContext(request))
    
@permission_required('adm.puede_eliminar_proyecto', login_url='access_denied')
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

@permission_required('adm.puede_visualizar_proyecto', login_url='access_denied')
def changes_report(request, id_project):
    """
    """
    project = Project.objects.get(id=id_project)
    phases = Phase.objects.filter(project_id=id_project)
    items = []
    modRequest = []
    
    for p in phases:
        items = items + list(Item.objects.filter(phase_id=p.id))
        
    for i in items:
        modRequest = modRequest + list(ModificationRequest.objects.filter(item_id=i.id))
        
    ctx = {'project':project, 'items':items, 'modRequest':modRequest}
    return render_to_response('adm/project/changes_report.html', ctx, context_instance=RequestContext(request))
    
def project_report(request, id_project):
    """
    """
    project = Project.objects.get(id=id_project)
    phases = Phase.objects.filter(project_id=id_project)
    items = []
    
    for p in phases:
        items = items + list(Item.objects.filter(phase_id=p.id))
        
    ctx = {'project':project, 'phases':phases, 'items':items}
    return render_to_response('adm/project/project_report.html', ctx, context_instance=RequestContext(request))
    
    