from __future__ import division # Float division
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
# Custom imports
from des.forms import ModifyItemForm, AssignIntegerForm, AssignStringForm, AssignBooleanForm, AssignDateForm
from models import ModificationRequest
from adm.models import Phase
from des.models import Item, Attribute
import forms
# Create your views here.

@permission_required('gdc.puede_visualizar_peticion_de_cambio', login_url='access_denied')
def list_requests(request):
    """
    Lista todas las peticiones recibidas.
    """
    user = request.user # Get logged in user
    requests = user.mod_requests_committee.all() # Get all modification requests to user
    ctx = {'requests':requests}
    return render(request, 'gdc/request/list_requests.html', ctx)

@permission_required('gdc.puede_crear_peticion_de_cambio', login_url='access_denied')
def create_request(request, id_item):
    """
    Crea una peticion de cambio.
    """
    
    def sum_cost(base_item):
        if base_item.status == Item.DELETED:
            cost = 0
        else:
            cost = base_item.cost
        children = base_item.successors.all()
        for c in children:
            cost = cost + sum_cost(c)
        return cost
    
    if request.method == "POST":
        form = forms.CreateModificationRequestForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            item = Item.objects.get(id=id_item)
            committee = item.phase.project.committee.all()
            total_requests = committee.count()
            cost = sum_cost(item)
            mod_request = ModificationRequest(title=title, item=item,requester=request.user, description=description, total_requests=total_requests, cost=cost)
            mod_request.save()
            for c in committee:
                mod_request.committee.add(c)
            ctx = {'id_project':item.phase.project.id,'id_phase':item.phase.id}
            return redirect(reverse('list_items', kwargs=ctx))
            
    if request.method == "GET":
        form = forms.CreateModificationRequestForm()
        item = Item.objects.get(id=id_item)
        ctx = {'id_project':item.phase.project.id,'id_phase':item.phase.id, 'form':form}
        return render(request, 'gdc/request/create_request.html', ctx)

@permission_required('gdc.puede_visualizar_peticion_de_cambio', login_url='access_denied')
def accept_request(request, id_request):
    """
    Aceptar una peticion.
    """
    
    if request.method == "GET":
        user = request.user
        mod_request = ModificationRequest.objects.get(id=id_request)
        mod_request.committee.remove(user)
        mod_request.accepted_requests += 1
        percentage = int(mod_request.accepted_requests / mod_request.total_requests * 100)
        if percentage >= 70: # If request is accepted by majority
            mod_request.voting = ModificationRequest.ACCEPTED
        elif mod_request.total_requests == mod_request.accepted_requests + mod_request.rejected_requests:
            mod_request.voting = ModificationRequest.REJECTED
        mod_request.save()
        return redirect(reverse('list_requests'))

@permission_required('gdc.puede_visualizar_peticion_de_cambio', login_url='access_denied')
def reject_request(request, id_request):
    """
    Rechazar una peticion.
    """
    if request.method == "GET":
        user = request.user
        mod_request = ModificationRequest.objects.get(id=id_request)
        mod_request.committee.remove(user)
        mod_request.rejected_requests += 1
        percentage = int(mod_request.rejected_requests / mod_request.total_requests * 100)
        if percentage >= 30:
            mod_request.voting = ModificationRequest.REJECTED
        elif mod_request.total_requests == mod_request.accepted_requests + mod_request.rejected_requests:
            mod_request.voting = ModificationRequest.REJECTED
        mod_request.save()
        return redirect(reverse('list_requests'))
    
@permission_required('gdc.puede_visualizar_peticion_de_cambio', login_url='access_denied')       
def visualize_request(request, id_request):
    mod_request = ModificationRequest.objects.get(id=id_request)
    ctx = {'mod_request':mod_request}
    return render(request, 'gdc/request/visualize_request.html', ctx)

@permission_required('gdc.puede_visualizar_peticion_de_cambio', login_url='access_denied')
def list_pending(request):
    """
    Lista los items peticionados
    """
    if request.method == "GET":
        items = Item.objects.filter(mod_requests__requester=request.user, mod_requests__voting=ModificationRequest.ACCEPTED)
        ctx = {'items':items}
        return render(request, 'gdc/request/list_pending.html', ctx)
    
@permission_required('des.puede_modificar_item', login_url='access_denied')  
def modify_pending_item(request, id_item):
    """
    Modificar item peticionado
    """
    item = Item.objects.get(id=id_item)
    if request.method == "POST":
        form = ModifyItemForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            cost = form.cleaned_data['cost']
            item.name = name
            item.description = description
            item.cost = cost
            item.save()
            return redirect('list_pending')
            
    if request.method == "GET":
        form = ModifyItemForm(initial={
            'name': item.name,
            'description':item.description,
            })
    ctx = {'form': form}
    return render(request, 'gdc/request/modify_pending_item.html', ctx)

@permission_required('des.puede_modificar_item', login_url='access_denied')  
def list_pending_attr(request, id_item):
    """
    Listar atributos del item peticionado
    """
    item = Item.objects.get(id=id_item)
    attr = item.attribute_set.all()
    ctx = {'attr':attr}
    return render(request, 'gdc/request/list_pending_attr.html', ctx)

@permission_required('des.puede_modificar_item', login_url='access_denied')  
def set_pending_attr_value(request, id_attr):
    """
    Asigna un valor al Atributo.
    """
    attribute = Attribute.objects.get(id=id_attr)
    
    if attribute.type == 'Numerico':
        
        if request.method == "POST":
            form = AssignIntegerForm(request.POST)
            if form.is_valid():
                attr_int = form.cleaned_data['attr_int']
                attribute.attr_int = attr_int
                attribute.save()
                ctx = {'id_item':attribute.item.id }
                return redirect(reverse('list_pending_attr', kwargs=ctx))
            
        if request.method == "GET":
            form = AssignIntegerForm(initial={
                'attr_int': attribute.attr_int,
            })
            ctx = {'form':form, 'id_item':attribute.item.id}
            return render(request, 'gdc/request/set_pending_attr_value.html', ctx)
        
    elif attribute.type == 'Cadena':
        
        if request.method == "POST":
            form = AssignStringForm(request.POST)
            if form.is_valid():
                attr_str = form.cleaned_data['attr_str']
                attribute.attr_str = attr_str
                attribute.save()
                ctx = {'id_item':attribute.item.id}
                return redirect(reverse('list_pending_attr', kwargs=ctx))
            
        if request.method == "GET":
            form = AssignStringForm(initial={
                'attr_str': attribute.attr_str,
            })    
            ctx = {'form':form, 'id_item':attribute.item.id}
            return render(request, 'gdc/request/set_pending_attr_value.html', ctx)
    
    elif attribute.type == 'Booleano':
        
        if request.method == "POST":
            form = AssignBooleanForm(request.POST)
            if form.is_valid():
                attr_bool = form.cleaned_data['attr_bool']
                attribute.attr_bool = attr_bool
                attribute.save()
                ctx = {'id_item':attribute.item.id}
                return redirect(reverse('list_pending_attr', kwargs=ctx))
            
        if request.method == "GET":
            form = AssignBooleanForm(initial={
                'attr_bool': attribute.attr_bool,
            })
            ctx = {'form':form, 'id_item':attribute.item.id}
            return render(request, 'gdc/request/set_pending_attr_value.html', ctx)
    
    else:
        
        if request.method == "POST":
            form = AssignDateForm(request.POST)
            if form.is_valid():
                attr_date = form.cleaned_data['attr_date']
                attribute.attr_date = attr_date
                attribute.save()
                ctx = {'id_item':attribute.item.id}
                return redirect(reverse('list_pending_attr', kwargs=ctx))
            
        if request.method == "GET":
            if attribute.attr_date != None:
                form = AssignDateForm(initial={
                    'attr_date': attribute.attr_date,
                })
            else:
                form = AssignDateForm()
            ctx = {'form':form, 'id_item':attribute.item.id}
            return render(request, 'gdc/request/set_pending_attr_value.html', ctx)
        
@permission_required('des.puede_asignar_item', login_url='access_denied')  
def list_pending_predecessors(request, id_item):
    """
    """
    if request.method == "GET":
        item = Item.objects.get(id=id_item)
        actual_phase = Phase.objects.get(id=item.phase.id)
        order = actual_phase.order - 1
        valid = False
        if(order >= 1): # If there is a previous phase
            valid = True
            previous_phase = Phase.objects.get(project=actual_phase.project, order=order)
            previous_items = Item.objects.filter(phase=previous_phase)
            ctx={'item':item, 'prev_items':previous_items, 'valid':valid}
        else:
            ctx={'item':item, 'valid':valid}
        return render(request, 'gdc/request/list_pending_predecessors.html', ctx)

@permission_required('des.puede_asignar_item', login_url='access_denied')  
def set_pending_predecessor(request, id_item, id_pred):
    """
    """
    if request.method == "GET":
        item = Item.objects.get(id=id_item)
        pred = Item.objects.get(id=id_pred)
        item.predecessor = pred
        item.save()
        ctx = {'id_item':id_item}
        return redirect(reverse('list_pending_predecessors', kwargs=ctx))

@permission_required('des.puede_asignar_item', login_url='access_denied') 
def unset_pending_predecessor(request, id_item):
    """
    """
    if request.method == "GET":
        item = Item.objects.get(id=id_item)
        item.predecessor = None
        item.save()
        ctx = {'id_item':id_item}
        return redirect(reverse('list_pending_predecessors', kwargs=ctx))

@permission_required('des.puede_asignar_item', login_url='access_denied')  
def list_pending_fathers(request, id_item):
    """
    """
    if request.method == "GET":
        item = Item.objects.get(id=id_item)
        item_fs = Item.objects.filter(phase=item.phase).exclude(id=id_item)
        valid = False
        if item_fs:
            valid = True
        ctx = {'item_fs':item_fs, 'valid':valid, 'item':item}
        return render(request, 'gdc/request/list_pending_fathers.html', ctx)

@permission_required('des.puede_asignar_item', login_url='access_denied')   
def set_pending_father(request, id_item, id_father):
    """
    """
    # Function that search cycles by DFS
    def check_acyclic(base_id, item_id):
        item = Item.objects.get(id=item_id)
        successors = item.successors.all()
        is_acyclic = True
        for s in successors:  # Get every successors
            if s.id == base_id:  # If successor is the base item, return False (cyclic)
                is_acyclic = False
            elif is_acyclic:  # Else, check his successors in recursion.
                is_acyclic = check_acyclic(base_id, s.id)
        return is_acyclic  # If none of them returned False, then return True
    
    if request.method == "GET":
        acyclic = check_acyclic(int(id_father), id_item)
        item = Item.objects.get(id=id_item)
        if acyclic:
            father = Item.objects.get(id=id_father)
            item.predecessor = father
            item.save()
        ctx = {'id_item':id_item}
        return redirect(reverse('list_pending_fathers', kwargs=ctx))

@permission_required('des.puede_asignar_item', login_url='access_denied') 
def unset_pending_father(request, id_item):
    """
    """
    if request.method == "GET":
        item = Item.objects.get(id=id_item)
        item.predecessor = None
        item.save()
        ctx = {'id_item':id_item}
        return redirect(reverse('list_pending_fathers', kwargs=ctx))
    
@permission_required('gdc.puede_visualizar_peticion_de_cambio', login_url='access_denied')
def finish_pending_item(request, id_item):
    """
    """
    if request.method == "GET":
        item = Item.objects.get(id=id_item)
        mod_request = ModificationRequest.objects.get(item=item)
        mod_request.voting = ModificationRequest.MODIFIED
        mod_request.save()
        return redirect('list_pending')