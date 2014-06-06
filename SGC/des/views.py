# -*- coding: utf-8 -*-
from django.db import transaction
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from adm.models import Project, Phase
from des.models import AttributeType, Attribute, ItemType, Item, BaseLine
from des import forms
import reversion
from reversion.models import Version

# Create your views here.
@permission_required('des.puede_visualizar_tipo_de_atributo', login_url='access_denied')
def list_attribute_types(request):
    """
    Función que lista los Tipos de Atributos existentes en el Sistema.
    """
    if request.method == "GET":
        attribute_types = AttributeType.objects.all()
        ctx = {'attribute_types':attribute_types}
        return render(request, 'des/attribute_type/list_attribute_types.html', ctx)

@permission_required('des.puede_crear_tipo_de_atributo', login_url='access_denied')
def create_attribute_type(request):
    """
    Función que crea un Tipo de Atributo y lo almacena en el Sistema.
    """
    type_parse = {
               "0": "Numerico",
               "1": "Cadena",
               "2": "Booleano",
               "3": "Fecha",
    }
    form = forms.CreateAttributeTypeForm()
    if request.method == "POST":
        form = forms.CreateAttributeTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            attr_type = form.cleaned_data['attr_type']
            attribute_type = AttributeType(name=name, description=description, attr_type=type_parse[attr_type])
            attribute_type.save()
            return redirect('list_attribute_types')
        else:
            ctx = {'form':form}
            return render(request, 'des/attribute_type/create_attribute_type.html', ctx)
    ctx = {'form':form}
    return render(request, 'des/attribute_type/create_attribute_type.html', ctx)

@permission_required('des.puede_modificar_tipo_de_atributo', login_url='access_denied')
def modify_attribute_type(request, id_attribute_type):
    """
    Función que modifica un Tipo de Atributo seleccionado del Sistema.
    """
    type_parse = {
               "0": "Numerico",
               "1": "Cadena",
               "2": "Booleano",
               "3": "Fecha",
    }
    attribute_type = AttributeType.objects.get(id=id_attribute_type)
    
    if request.method == "POST":
        form = forms.ModifyAttributeTypeForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            attr_type = form.cleaned_data['attr_type']
            attribute_type.name = name
            attribute_type.description = description
            attribute_type.attr_type = type_parse[attr_type]
            attribute_type.save()
            return redirect('list_attribute_types')
            
    if request.method == "GET":
        form = forms.ModifyAttributeTypeForm(initial={
            'name': attribute_type.name,
            'description':attribute_type.description,
            'attr_type':attribute_type.attr_type,
            })
    ctx = {'form': form, 'attribute_type': attribute_type}
    return render(request, 'des/attribute_type/modify_attribute_type.html', ctx)

@permission_required('des.puede_eliminar_tipo_de_atributo', login_url='access_denied')
def delete_attribute_type(request, id_attribute_type):
    """
    Función que elimina un Tipo de Atributo del Sistema.
    """
    attribute_type = AttributeType.objects.get(id=id_attribute_type)
    # POST
    if request.method == "POST":
        attribute_type.delete()
        return redirect('list_attribute_types')
    # GET
    if request.method == "GET":
        ctx = {'attribute_type':attribute_type}
        return render(request, 'des/attribute_type/delete_attribute_type.html', ctx)

@permission_required('des.puede_visualizar_tipo_de_atributo', login_url='access_denied')  
def visualize_attribute_type(request, id_attribute_type):
    """
    Función que despliega los campos de un Tipo de Atributo.
    """
    attribute_type = AttributeType.objects.get(id=id_attribute_type)
    ctx = {'attribute_type': attribute_type}
    return render(request, 'des/attribute_type/visualize_attribute_type.html', ctx)

@permission_required('des.puede_visualizar_tipo_de_item', login_url='access_denied')
def list_item_types(request):
    """
    Función que lista los Tipo de Ítems existentes en el Sistema.
    """
    item_ts = ItemType.objects.all()
    ctx = {'item_ts':item_ts}
    return render(request, 'des/item_type/list_item_types.html', ctx)

@permission_required('des.puede_crear_tipo_de_item', login_url='access_denied')
def create_item_type(request):
    """
    Función que crea un Tipo de Ítem y lo almacena en el Sistema.
    """
    form = forms.CreateItemTypeForm()
    # POST
    if request.method == "POST":
        form = forms.CreateItemTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            item_t = ItemType(name=name, description=description)
            item_t.save()
            return redirect('list_item_types')
    ctx = {'form':form}
    return render(request, 'des/item_type/create_item_type.html', ctx)

@permission_required('des.puede_modificar_tipo_de_item', login_url='access_denied')
def modify_item_type(request, id_item_type):
    """
    Función que modifica un Tipo de Ítem del Sistema.
    """
    item_t = ItemType.objects.get(id=id_item_type)
    if request.method == "POST":
        form = forms.ModifyItemTypeForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            item_t.name = name
            item_t.description = description
            item_t.save()
            return redirect('list_item_types')
            
    if request.method == "GET":
        form = forms.ModifyItemTypeForm(initial={
            'name': item_t.name,
            'description':item_t.description,
            })
        ctx = {'form': form, 'item_t': item_t}
        return render(request, 'des/item_type/modify_item_type.html', ctx)

@permission_required('des.puede_eliminar_tipo_de_item', login_url='access_denied')
def delete_item_type(request, id_item_type):
    """
    Función que elimina un Tipo de Ítem del Sistema.
    """
    item_t = ItemType.objects.get(id=id_item_type)
    if request.method == "POST":
        item_t.delete()
        return redirect('list_item_types')
    # GET
    if request.method == "GET":
        ctx = {'item_t':item_t}
        return render(request, 'des/item_type/delete_item_type.html', ctx)

@permission_required('des.puede_visualizar_tipo_de_item', login_url='access_denied')
def visualize_item_type(request, id_item_type):
    """
    Función que despliega los campos de un Tipo de Ítem.
    """
    item_t = ItemType.objects.get(id=id_item_type)
    attr_types = item_t.attribute_types.all()
    ctx = {'item_t': item_t, 'attr_types':attr_types}
    return render(request, 'des/item_type/visualize_item_type.html', ctx)

@permission_required('des.puede_asignar_tipo_de_atributo', login_url='access_denied')
def assign_attribute_type(request, id_item_type):
    """
    Función que despliega todos los Tipo de Atributos disponibles en el sistema para ser asignados/desasignados 
    por por Tipo de Ítem seleccionado.
    """
    attr_t = AttributeType.objects.all()
    item_t = ItemType.objects.get(id=id_item_type)
    ctx = {'item_t':item_t, 'attr_t':attr_t}
    return render(request, 'des/item_type/assign_attribute_type.html', ctx)

@permission_required('des.puede_asignar_tipo_de_atributo', login_url='access_denied')
def grant_attribute_type(request, id_item_type, id_attr_type):
    """
    Función que asigna un Atributo al Tipo de Ítem.
    """
    item_t = ItemType.objects.get(id=id_item_type)
    attr_t = AttributeType.objects.get(id=id_attr_type)
    new_attr_t = False
    try:
        attr_t = item_t.attribute_types.get(id=id_attr_type)
    except AttributeType.DoesNotExist:
        new_attr_t = True      
    if new_attr_t:
        item_t.attribute_types.add(attr_t)
        item_t.save()
    ctx = {'id_item_type':id_item_type}
    return redirect(reverse('assign_attribute_type', kwargs=ctx))

@permission_required('des.puede_asignar_tipo_de_atributo', login_url='access_denied')
def deny_attribute_type(request, id_item_type, id_attr_type):
    """
    Función que desasigna un Atributo al Tipo de Ítem.
    """
    item_t = ItemType.objects.get(id=id_item_type)
    attr_t = AttributeType.objects.get(id=id_attr_type)
    item_t.attribute_types.remove(attr_t)
    item_t.save()
    ctx = {'id_item_type':id_item_type}
    return redirect(reverse('assign_attribute_type', kwargs=ctx))

@permission_required('des.puede_visualizar_item', login_url='access_denied')
def list_items(request, id_project, id_phase):
    """
    Función que visualiza todos los Ítems del Sistema.
    """
    if request.method == "GET":
        phase = Phase.objects.get(id=id_phase)
        items = Item.objects.exclude(status=Item.DELETED).filter(phase=phase)
        ctx = {'items':items, 'id_project':id_project, 'id_phase':id_phase}
        return render(request, 'des/item/list_items.html', ctx)

@permission_required('des.puede_crear_item', login_url='access_denied')
@transaction.atomic()
@reversion.create_revision()
def create_item(request, id_project, id_phase):
    """
    Función que crea un Ítem y lo almacena en el Sistema.
    """
    if request.method == "GET":
        form = forms.CreateItemForm()
        ctx = {'form':form, 'id_project':id_project, 'id_phase':id_phase}
        return render(request, 'des/item/create_item.html', ctx)
    
    if request.method == "POST":
        form = forms.CreateItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            cost = form.cleaned_data['cost']
            phase = Phase.objects.get(id=id_phase)
            Item.objects.create(name=name, description=description, cost=cost, phase=phase)
            ctx = {'id_project':id_project, 'id_phase':id_phase}
            return redirect(reverse('list_items', kwargs=ctx))
        else:
            ctx = {'form':form, 'id_project':id_project, 'id_phase':id_phase}
            return render(request, 'des/item/create_item.html', ctx)
 
@permission_required('des.puede_modificar_item', login_url='access_denied')
@transaction.atomic()
@reversion.create_revision()   
def modify_item(request, id_item, id_project, id_phase):
    """
    Función que modifica los datos del Ítem seleccionado. El Ítem deberá estar activo para poder ser modificado.
    Si el Ítem se encuentra cerrado. Se debe de crear una Petición de Cambio para hacer los cambios
    pertinentes.
    """
    item = Item.objects.get(id=id_item)
    
    if request.method == "GET":
        form = forms.ModifyItemForm(initial={
            'name': item.name,
            'description':item.description,
            'cost':item.cost,
            })
        ctx = {'form': form, 'item': item, 'id_project':id_project, 'id_phase':id_phase}
        return render(request, 'des/item/modify_item.html', ctx)
    
    if request.method == "POST":
        form = forms.ModifyItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            cost = form.cleaned_data['cost']
            item.name = name
            item.description = description
            item.cost = cost
            item.save()
            ctx = {'id_project':id_project, 'id_phase':id_phase}
            return redirect(reverse('list_items', kwargs=ctx))
        else:
            ctx = {'form': form, 'item': item, 'id_project':id_project, 'id_phase':id_phase}
            return render(request, 'des/item/modify_item.html', ctx)
    
@permission_required('des.puede_eliminar_item', login_url='access_denied')
@transaction.atomic()
@reversion.create_revision()
def delete_item(request, id_item, id_project, id_phase):
    """
    Función que elimina lógicamente el Ítem seleccionado. El Ítem deberá estar activo para poder ser eliminado.
    Si el Ítem se encuentra cerrado, se debe de crear una Petición de Cambio para hacer los cambios
    pertinentes.
    """
    item = Item.objects.get(id=id_item)
    
    if request.method == "GET":    
        ctx = {'item':item, 'id_project':id_project, 'id_phase':id_phase}
        return render(request, 'des/item/delete_item.html', ctx)
    
    if request.method == "POST":
        item.status = Item.DELETED
        item.save()
        ctx = {'id_project':id_project, 'id_phase':id_phase}
        return redirect(reverse('list_items', kwargs=ctx))
    
@permission_required('des.puede_asignar_tipo_de_item', login_url='access_denied')
def assign_item_type(request, id_item, id_project, id_phase):
    """
    Función que lista los Tipo de Ítems asignables al Ítem seleccionado. El usuario debe seleccionar el botón
    al lado derecho para Asignar/Quitar el Tipo de Ítem. Si el Ítem ya tiene un Tipo de Ítem seleccionado, solo
    podrá visualizar el Tipo de Ítem seleccionado.
    """
    
    item_types = ItemType.objects.all()
    item = Item.objects.get(id=id_item)
    valid = True
    if item.attribute_set.exists():  # If item has attributes
        valid = False
    ctx = {'item':item, 'item_types':item_types, 'valid':valid, 'id_project':id_project, 'id_phase':id_phase}
    return render(request, 'des/item/assign_item_type.html', ctx)

@permission_required('des.puede_asignar_tipo_de_item', login_url='access_denied')
def add_item_type(request, id_item, id_item_type, id_project, id_phase):
    """
    Función que asigna el Tipo de Item al Item seleccionado. El Item sera la instancia del Tipo de Items con
    sus respectivos atributos.
    """
    item = Item.objects.get(id=id_item)
    item_type = ItemType.objects.get(id=id_item_type)
    if not item.attribute_set.exists():  # If there is already some attributes in the queryset... Double assignment error solved here.
        for a in item_type.attribute_types.all():  # Create all attribute skeletons to item
            Attribute.objects.create(name=a.name, description=a.description, type=a.attr_type, item=item)
    ctx = {'item':item, 'item_type':item_type, 'id_project':id_project, 'id_phase':id_phase}
    return render(request, 'des/item/add_item_type.html', ctx)

@permission_required('des.puede_visualizar_atributo', login_url='access_denied')
def list_attributes(request, id_item, id_project, id_phase):
    item = Item.objects.get(id=id_item)
    attr = item.attribute_set.all()
    ctx = {'item':item, 'attr':attr, 'id_project':id_project, 'id_phase':id_phase}
    return render(request, 'des/attribute/list_attributes.html', ctx)

@permission_required('des.puede_modificar_atributo', login_url='access_denied')
def set_attribute_value(request, id_item, id_attr, id_project, id_phase):
    """
    Asigna un valor al Atributo.
    """
    attribute = Attribute.objects.get(id=id_attr)
    item = Item.objects.get(id=id_item)
    if attribute.type == 'Numerico':
        form = forms.AssignIntegerForm()
        if request.method == "POST":
            form = forms.AssignIntegerForm(request.POST)
            if form.is_valid():
                attr_int = form.cleaned_data['attr_int']
                attribute.attr_int = attr_int
                attribute.save()
                ctx = {'id_item':id_item, 'id_project':id_project, 'id_phase':id_phase}
                return HttpResponseRedirect(reverse('list_attributes', kwargs=ctx))
            else:
                ctx = {'form':form, 'item':item, 'id_project':id_project, 'id_phase':id_phase}
                return render_to_response('des/attribute/set_attribute_value.html', ctx, context_instance=RequestContext(request))
        if request.method == "GET":
            form = forms.AssignIntegerForm(initial={
                'item': item,
            })
        ctx = {'form':form, 'item':item, 'id_project':id_project, 'id_phase':id_phase}
        return render_to_response('des/attribute/set_attribute_value.html', ctx, context_instance=RequestContext(request))
        
    elif attribute.type == 'Cadena':
        
        form = forms.AssignStringForm()
        if request.method == "POST":
            form = forms.AssignStringForm(request.POST)
            if form.is_valid():
                attr_str = form.cleaned_data['attr_str']
                attribute.attr_str = attr_str
                attribute.save()
                ctx = {'id_item':id_item, 'id_project':id_project, 'id_phase':id_phase}
                return HttpResponseRedirect(reverse('list_attributes', kwargs=ctx))
            else:
                ctx = {'form':form, 'item':item, 'id_project':id_project, 'id_phase':id_phase}
                return render_to_response('des/attribute/set_attribute_value.html', ctx, context_instance=RequestContext(request))
        if request.method == "GET":
            form = forms.AssignStringForm(initial={
                'item': item,
            })    
        ctx = {'form':form, 'item':item, 'id_project':id_project, 'id_phase':id_phase}
        return render_to_response('des/attribute/set_attribute_value.html', ctx, context_instance=RequestContext(request))
    
    elif attribute.type == 'Booleano':
        
        form = forms.AssignBooleanForm()
        if request.method == "POST":
            form = forms.AssignBooleanForm(request.POST)
            if form.is_valid():
                attr_bool = form.cleaned_data['attr_bool']
                attribute.attr_bool = attr_bool
                attribute.save()
                ctx = {'id_item':id_item, 'id_project':id_project, 'id_phase':id_phase}
                return HttpResponseRedirect(reverse('list_attributes', kwargs=ctx))
            else:
                ctx = {'form':form, 'item':item, 'id_project':id_project, 'id_phase':id_phase}
                return render_to_response('des/attribute/set_attribute_value.html', ctx, context_instance=RequestContext(request))
        if request.method == "GET":
            form = forms.AssignBooleanForm(initial={
                'item': item,
            })
        ctx = {'form':form, 'item':item, 'id_project':id_project, 'id_phase':id_phase}
        return render_to_response('des/attribute/set_attribute_value.html', ctx, context_instance=RequestContext(request))
    
    else:
        
        form = forms.AssignDateForm()
        if request.method == "POST":
            form = forms.AssignDateForm(request.POST)
            if form.is_valid():
                attr_date = form.cleaned_data['attr_date']
                attribute.attr_date = attr_date
                attribute.save()
                ctx = {'id_item':id_item, 'id_project':id_project, 'id_phase':id_phase}
                return HttpResponseRedirect(reverse('list_attributes', kwargs=ctx))
            else:
                ctx = {'form':form, 'item':item, 'id_project':id_project, 'id_phase':id_phase}
                return render_to_response('des/attribute/set_attribute_value.html', ctx, context_instance=RequestContext(request))
            if request.method == "GET":
                form = forms.AssignDateForm(initial={
                    'item': item,
                })
        ctx = {'form':form, 'item':item, 'id_project':id_project, 'id_phase':id_phase}
        return render_to_response('des/attribute/set_attribute_value.html', ctx, context_instance=RequestContext(request))

@permission_required('des.puede_modificar_item', login_url='access_denied')
def item_history(request, id_item, id_project, id_phase):
    item = Item.objects.get(id=id_item)
    # Build a list of all previous versions, latest versions first:
    version_list = reversion.get_for_object(item)   
    ctx = {'item':item, 'version_list':version_list, 'id_project':id_project, 'id_phase':id_phase}
    return render(request, 'des/item/item_history.html', ctx)

@permission_required('des.puede_modificar_item', login_url='access_denied')
def revert_item(request, id_item, id_version, id_project, id_phase):
    item = Item.objects.get(id=id_item)
    version = Version.objects.get(id=id_version)
    version.revision.revert()
    ctx = {'item':item, 'id_project':id_project, 'id_phase':id_phase}
    return render(request, 'des/item/revert_item.html', ctx)

@permission_required('des.puede_visualizar_item', login_url='access_denied')
def list_deleted_items(request, id_project, id_phase):
    items = Item.objects.filter(status=Item.DELETED)
    ctx = {'items':items, 'id_project':id_project, 'id_phase':id_phase}
    return render(request, 'des/item/list_deleted_items.html', ctx)

@permission_required('des.puede_modificar_item', login_url='access_denied')
def revive_item(request, id_item, id_project, id_phase):
    item = Item.objects.get(id=id_item)
    item.status = Item.ACTIVE
    item.save()
    ctx = {'item':item, 'id_project':id_project, 'id_phase':id_phase}
    return render(request, 'des/item/revive_item.html', ctx)

@permission_required('des.puede_asignar_item', login_url='access_denied')
def list_predecessors(request, id_project, id_phase, id_item):
    """
    """
    actual_phase = Phase.objects.get(id=id_phase)
    order = actual_phase.order - 1
    valid = False
    item = Item.objects.get(id=id_item)
    if(order >= 1):  # If there is a previous phase
        valid = True
        previous_phase = Phase.objects.get(project=actual_phase.project, order=order)
        previous_items = Item.objects.filter(phase=previous_phase)
        ctx = {'prev_items':previous_items, 'item':item, 'id_item':id_item, 'id_project':id_project, 'id_phase':id_phase, 'valid':valid}
    else:
        ctx = {'id_item':id_item, 'id_project':id_project, 'id_phase':id_phase, 'valid':valid}
    return render(request, 'des/item/list_predecessors.html', ctx)
    
@permission_required('des.puede_asignar_item', login_url='access_denied')
def set_predecessor(request, id_project, id_phase, id_item, id_pred):
    """
    Funcion que asigna un antecesor al item.
    """
    if request.method == "GET":
        item = Item.objects.get(id=id_item)
        pred = Item.objects.get(id=id_pred)
        item.predecessor = pred
        item.save()
        ctx = {'predecessor':pred, 'item':item, 'id_item':id_item, 'id_project':id_project, 'id_phase':id_phase}
        return render(request, 'des/item/set_predecessor.html', ctx)

@permission_required('des.puede_asignar_item', login_url='access_denied')  
def list_fathers(request, id_project, id_phase, id_item):
    """
    Función que lista todos los ítems de la misma fase.
    """
    if request.method == "GET":
        phase = Phase.objects.get(id=id_phase)
        item_fs = Item.objects.filter(phase=phase).exclude(id=id_item)
        item = Item.objects.get(id=id_item)
        valid = False
        if item_fs:
            valid = True
        ctx = {'id_item':id_item, 'id_project':id_project, 'id_phase':id_phase, 'item_fs':item_fs, 'valid':valid, 'item':item}
        return render(request, 'des/item/list_fathers.html', ctx)

@permission_required('des.puede_asignar_item', login_url='access_denied')   
def set_father(request, id_item, id_father):
    """
    Función que asigna un padre para el item respectivo. Verifica internamente que el grafo sea acíclico.
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
        ctx = {'id_project':item.phase.project.id, 'id_phase':item.phase.id, 'id_item':id_item}
        return redirect(reverse('list_fathers', kwargs=ctx))

@permission_required('des.puede_asignar_item', login_url='access_denied')
def unset_father(request, id_item):
    """
    Función que deasigna el padre del ítem respectivo.
    """
    if request.method == "GET":
        item = Item.objects.get(id=id_item)
        item.predecessor = None
        item.save()
        ctx = {'id_project':item.phase.project.id, 'id_phase':item.phase.id, 'id_item':id_item}
        return redirect(reverse('list_fathers', kwargs=ctx))

@permission_required('des.puede_visualizar_item', login_url='access_denied')     
def calculate_cost(request, id_project, id_phase , id_item):
    """
    Suma recursivamente el costo total atravesando por depth-first
    """
    
    def sum_cost(base_item):
        if base_item:
            cost = base_item.cost
            children = base_item.successors.all()
            for i in children:  # For each succeeding items
                cost = cost + sum_cost(i)  # Sum his total cost
        return cost  # Return total cost of the tree
    
    base_item = Item.objects.get(id=id_item)
    cost = sum_cost(base_item)
    ctx = {'id_project':id_project, 'id_phase':id_phase, 'id_item':id_item, 'item':base_item, 'cost':cost}
    return render(request, 'des/item/calculate_cost.html', ctx)

@permission_required('adm.puede_visualizar_proyecto', login_url='access_denied')  
def list_user_projects(request):
    """
    """
    projects = request.user.projects.all()    
    ctx = {'projects':projects}
    return render(request, 'des/baseline/list_user_projects.html', ctx)

@permission_required('adm.puede_visualizar_fase', login_url='access_denied')
def list_project_phases(request, id_project):
    """
    """
    project = Project.objects.get(id=id_project)    
    phases = Phase.objects.filter(project_id=id_project)
    ctx = {'project':project, 'phases':phases}
    return render(request, 'des/baseline/list_project_phases.html', ctx)

@permission_required('des.puede_visualizar_linea_base', login_url='access_denied')
def list_phase_baseline(request, id_project, id_phase):
    """
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    baseline = BaseLine.objects.filter(phase_id=id_phase)
    ctx = {'project':project, 'phase':phase, 'baseline':baseline}
    return render(request, 'des/baseline/list_phase_baseline.html', ctx)

@permission_required('des.puede_crear_linea_base', login_url='access_denied')
def create_baseline(request, id_project, id_phase):
    """
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    form = forms.CreateBaseLineForm()
    
    if request.method == 'POST':        
        form = forms.CreateBaseLineForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']            
            baseline = BaseLine.objects.create(name=name, state=0, phase=phase)
            baseline.save()
            ctx = {'project':project, 'phase': phase, 'baseline':BaseLine.objects.filter(phase_id=id_phase)}            
            return render(request, 'des/baseline/list_phase_baseline.html', ctx)
        
        else:
            ctx = {'form':form, 'project':project, 'phase':phase}
            return render(request, 'des/baseline/create_baseline.html', ctx)
        
    ctx = {'form':form, 'project':project, 'phase':phase}
    return render(request, 'des/baseline/create_baseline.html', ctx)

@permission_required('des.puede_modificar_linea_base', login_url='access_denied')
def modify_baseline(request, id_project, id_phase, id_baseline):
    """
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    baseline = BaseLine.objects.get(id=id_baseline)
    
    if request.method == "POST":
        form = forms.ModifyBaseLineForm(data=request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            baseline.name = name
            baseline.save()            
            ctx = {'project':project, 'phase':phase, 'baseline':BaseLine.objects.filter(phase_id=id_phase)}            
            return render(request, 'des/baseline/list_phase_baseline.html', ctx)
            
    if request.method == "GET":
        form = forms.ModifyBaseLineForm(initial={
            'name' : baseline.name,
            })
    ctx = {'form': form, 'project':project, 'phase':phase, 'baseline':baseline}
    return render(request, 'des/baseline/modify_baseline.html', ctx)    

@permission_required('des.puede_modificar_linea_base', login_url='access_denied')
def modify_baseline_state(request, id_project, id_phase, id_baseline):
    """
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    baseline = BaseLine.objects.get(id=id_baseline)
    
    if request.method == "POST":
        form = forms.ModifyBaseLineStateForm(data=request.POST)
        
        if form.is_valid():
            state = form.cleaned_data['state']
            baseline.state = state
            baseline.save()            
            ctx = {'project':project, 'phase':phase, 'baseline':BaseLine.objects.filter(phase_id=id_phase)}            
            return render(request, 'des/baseline/list_phase_baseline.html', ctx)
            
    if request.method == "GET":
        form = forms.ModifyBaseLineStateForm(initial={
            'state' : baseline.state,
            })
    ctx = {'form': form, 'project':project, 'phase':phase, 'baseline':baseline}
    return render(request, 'des/baseline/modify_baseline_state.html', ctx)    

@permission_required('des.puede_asignar_item', login_url='access_denied')
def manage_baseline_items(request, id_project, id_phase, id_baseline):
    """
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    baseline = BaseLine.objects.get(id=id_baseline)
    items = Item.objects.filter(phase_id=id_phase).exclude(status=Item.DELETED)
    bsitems = Item.objects.filter(baseline_id=id_baseline)
    
    ctx = {'project':project, 'phase':phase, 'baseline':baseline, 'items':items, 'bsitems':bsitems}
    return render(request, 'des/baseline/manage_baseline_items.html', ctx)

@permission_required('des.puede_asignar_item', login_url='access_denied')
def assign_baseline_item(request, id_project, id_phase, id_baseline, id_item):
    """    
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    baseline = BaseLine.objects.get(id=id_baseline)
    item = Item.objects.get(id=id_item)
    items = Item.objects.filter(phase_id=id_phase).exclude(status=Item.DELETED)
    bsitems = Item.objects.filter(baseline_id=id_baseline)   

    if phase.order == 1:  # Primera fase.
        item.baseline_id = baseline.id
        item.status = Item.FINISHED
        item.save()        
    else:  # En las fases subsiguientes
        if item.predecessor != None:  # los items requieren predecesores.
            item.baseline_id = baseline.id
            item.status = Item.FINISHED
            item.save()
                
    ctx = {'project':project, 'phase':phase, 'baseline':baseline, 'items':items, 'bsitems':bsitems}
    return render(request, 'des/baseline/manage_baseline_items.html', ctx)

@permission_required('des.puede_asignar_item', login_url='access_denied')
def remove_baseline_item(request, id_project, id_phase, id_baseline, id_item):
    """    
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    baseline = BaseLine.objects.get(id=id_baseline)
    item = Item.objects.get(id=id_item)
    items = Item.objects.filter(phase_id=id_phase).exclude(status=Item.DELETED)
    bsitems = Item.objects.filter(baseline_id=id_baseline)    
       
    item.baseline_id = None
    item.status = Item.ACTIVE
    item.save()
    
    ctx = {'project':project, 'phase':phase, 'baseline':baseline, 'items':items, 'bsitems':bsitems}
    return render(request, 'des/baseline/manage_baseline_items.html', ctx)   

@permission_required('des.puede_eliminar_linea_base', login_url='access_denied')
def delete_baseline(request, id_project, id_phase, id_baseline):
    """
    """
    project = Project.objects.get(id=id_project)
    phase = Phase.objects.get(id=id_phase)
    baseline = BaseLine.objects.get(id=id_baseline)  
    
    if request.method == "POST":
        baseline.delete()
        ctx = {'project':project, 'phase':phase, 'baseline':BaseLine.objects.filter(phase_id=id_phase)}            
        return render(request, 'des/baseline/list_phase_baseline.html', ctx)
   
    if request.method == "GET":
        ctx = {'project':project, 'phase':phase, 'baseline':baseline}
        return render(request, 'des/baseline/delete_baseline.html', ctx)
