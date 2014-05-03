from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from des.models import AttributeType, Attribute, ItemType
from des import forms
# Create your views here.
@login_required(login_url='/login/')
def list_attribute_types(request):
    """
    Lista los tipos de atributos existentes en el sistema.
    """
    attribute_types = AttributeType.objects.all()
    ctx = {'attribute_types':attribute_types}
    return render_to_response('des/attribute_type/list_attribute_types.html', ctx, context_instance=RequestContext(request))

def create_attribute_type(request):
    """
    Crea un tipo de atributo y lo almacena en el sistema.
    """
    form = forms.CreateAttributeTypeForm()
    if request.method == "POST":
        form = forms.CreateAttributeTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            choice = form.cleaned_data['choice']
            attribute_type = AttributeType(name=name, description=description, choice=choice)
            attribute_type.save()
            return HttpResponseRedirect('/des/list_attribute_types/')
        else:
            ctx = {'form':form}
            return render_to_response('des/attribute_type/create_attribute_type.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('des/attribute_type/create_attribute_type.html', ctx, context_instance=RequestContext(request))
    
def modify_attribute_type(request, id_attribute_type):
    """
    Modifica un tipo de attribute del sistema.
    """
    attribute_type = AttributeType.objects.get(id=id_attribute_type)
    if request.method == "POST":
        form = forms.ModifyAttributeTypeForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            attribute_type.name = name
            attribute_type.description = description
            attribute_type.save()
            return HttpResponseRedirect('/des/list_attribute_types/')
            
    if request.method == "GET":
        form = forms.ModifyAttributeTypeForm(initial={
            'name': attribute_type.name,
            'description':attribute_type.description,
            })
    ctx = {'form': form, 'attribute_type': attribute_type}
    return render_to_response('des/attribute_type/modify_attribute_type.html', ctx, context_instance=RequestContext(request))

def delete_attribute_type(request, id_attribute_type):
    """
    Elimina un tipo de attribute del sistema.
    """
    attribute_type = AttributeType.objects.get(id=id_attribute_type)
    if request.method == "POST":
        attribute_type.delete()
        return HttpResponseRedirect('/des/list_attribute_types/')
    if request.method == "GET":
        ctx = {'attribute_type':attribute_type}
        return render_to_response('des/attribute_type/delete_attribute_type.html', ctx, context_instance=RequestContext(request))
    
def visualize_attribute_type(request, id_attribute_type):
    """
    Despliega los campos de un tipo de atributo.
    """
    attribute_type = AttributeType.objects.get(id=id_attribute_type)
    ctx = {'attribute_type': attribute_type}
    return render_to_response('des/attribute_type/visualize_attribute_type.html', ctx, context_instance=RequestContext(request))

def list_attributes(request):
    """
    Lista los atributos existentes en el sistema.
    """
    attributes = Attribute.objects.all()
    ctx = {'attributes':attributes}
    return render_to_response('des/attribute/list_attributes.html', ctx, context_instance=RequestContext(request))

def create_attribute(request):
    """
    Crea un atributo y lo almacena en el sistema.
    """
    form = forms.CreateAttributeForm()
    if request.method == "POST":
        form = forms.CreateAttributeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            attribute = Attribute(name=name, description=description)
            attribute.save()
            return HttpResponseRedirect('/des/list_attributes/')
        else:
            ctx = {'form':form}
            return render_to_response('des/attribute/create_attribute.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('des/attribute/create_attribute.html', ctx, context_instance=RequestContext(request))
    
def modify_attribute(request, id_attribute):
    """
    Modifica un atributo del sistema.
    """
    attribute = Attribute.objects.get(id=id_attribute)
    if request.method == "POST":
        form = forms.ModifyAttributeForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            attribute.name = name
            attribute.description = description
            attribute.save()
            return HttpResponseRedirect('/des/list_attributes/')
            
    if request.method == "GET":
        form = forms.ModifyAttributeForm(initial={
            'name': attribute.name,
            'description':attribute.description,
            })
    ctx = {'form': form, 'attribute': attribute}
    return render_to_response('des/attribute/modify_attribute.html', ctx, context_instance=RequestContext(request))

def delete_attribute(request, id_attribute):
    """
    Elimina un atributo del sistema.
    """
    attribute = Attribute.objects.get(id=id_attribute)
    if request.method == "POST":
        attribute.delete()
        return HttpResponseRedirect('/des/list_attributes/')
    if request.method == "GET":
        ctx = {'attribute':attribute}
        return render_to_response('des/attribute/delete_attribute.html', ctx, context_instance=RequestContext(request))

def visualize_attribute(request, id_attribute):
    """
    Despliega los campos de un atributo.
    """
    attribute = Attribute.objects.get(id=id_attribute)
    ctx = {'attribute': attribute}
    return render_to_response('des/attribute/visualize_attribute.html', ctx, context_instance=RequestContext(request))

def assign_attribute_type(request, id_attribute):
    attribute = Attribute.objects.get(id=id_attribute)
    attribute_types = AttributeType.objects.all()
    ctx = {'attribute':attribute, 'attribute_types':attribute_types}
    return render_to_response('des/attribute/assign_attribute_type.html', ctx, context_instance=RequestContext(request))

def grant_attribute_type(request, id_attribute, id_attribute_type):
    attribute = Attribute.objects.get(id=id_attribute)
    attribute_type = AttributeType.objects.get(id=id_attribute_type)
    attribute.type = attribute_type
    attribute.save()
    ctx = {'attribute':attribute, 'attribute_type':attribute_type}
    return render_to_response('des/attribute/grant_attribute_type.html', ctx, context_instance=RequestContext(request))

def assign_attribute_value(request, id_attribute):
    """
    Asigna un valor al tipo de attribute.
    """
    attribute = Attribute.objects.get(id=id_attribute)
    
    if attribute.type.choice == 0:
        form = forms.AssignIntegerForm()
        if request.method == "POST":
            form = forms.AssignIntegerForm(request.POST)
            if form.is_valid():
                attr_int = form.cleaned_data['attr_int']
                attribute.attr_int = attr_int
                attribute.save()
                return HttpResponseRedirect('/des/list_attributes/')
            else:
                ctx = {'form':form}
                return render_to_response('des/attribute/assign_attribute_value.html', ctx, context_instance=RequestContext(request))
        ctx = {'form':form}
        return render_to_response('des/attribute/assign_attribute_value.html', ctx, context_instance=RequestContext(request))
    
    elif attribute.type.choice == 1:
        
        form = forms.AssignStringForm()
        if request.method == "POST":
            form = forms.AssignStringForm(request.POST)
            if form.is_valid():
                attr_str = form.cleaned_data['attr_str']
                attribute.attr_str = attr_str
                attribute.save()
                return HttpResponseRedirect('/des/list_attributes/')
            else:
                ctx = {'form':form}
                return render_to_response('des/attribute/assign_attribute_value.html', ctx, context_instance=RequestContext(request))
        ctx = {'form':form}
        return render_to_response('des/attribute/assign_attribute_value.html', ctx, context_instance=RequestContext(request))
    
    elif attribute.type.choice == 2:
        
        form = forms.AssignBooleanForm()
        if request.method == "POST":
            form = forms.AssignBooleanForm(request.POST)
            if form.is_valid():
                attr_bool = form.cleaned_data['attr_bool']
                attribute.attr_bool = attr_bool
                attribute.save()
                return HttpResponseRedirect('/des/list_attributes/')
            else:
                ctx = {'form':form}
                return render_to_response('des/attribute/assign_attribute_value.html', ctx, context_instance=RequestContext(request))
        ctx = {'form':form}
        return render_to_response('des/attribute/assign_attribute_value.html', ctx, context_instance=RequestContext(request))
    
    else:
        
        form = forms.AssignDateForm()
        if request.method == "POST":
            form = forms.AssignDateForm(request.POST)
            if form.is_valid():
                attr_date = form.cleaned_data['attr_date']
                attribute.attr_date = attr_date
                attribute.save()
                return HttpResponseRedirect('/des/list_attributes/')
            else:
                ctx = {'form':form}
                return render_to_response('des/attribute/assign_attribute_value.html', ctx, context_instance=RequestContext(request))
        ctx = {'form':form}
        return render_to_response('des/attribute/assign_attribute_value.html', ctx, context_instance=RequestContext(request))

def list_item_types(request):
    """
    Lista los tipos de atributos existentes en el sistema.
    """
    item_ts = ItemType.objects.all()
    ctx = {'item_ts':item_ts}
    return render_to_response('des/item_type/list_item_types.html', ctx, context_instance=RequestContext(request))

def create_item_type(request):
    """
    Crea un tipo de item y lo almacena en el sistema.
    """
    form = forms.CreateItemTypeForm()
    if request.method == "POST":
        form = forms.CreateItemTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            item_t = ItemType(name=name, description=description)
            item_t.save()
            return HttpResponseRedirect('/des/list_item_types/')
        else:
            ctx = {'form':form}
            return render_to_response('des/item_type/create_item_type.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('des/item_type/create_item_type.html', ctx, context_instance=RequestContext(request))
    
def modify_item_type(request, id_item_type):
    """
    Modifica un tipo de item del sistema.
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
            return HttpResponseRedirect('/des/list_item_types/')
            
    if request.method == "GET":
        form = forms.ModifyItemTypeForm(initial={
            'name': item_t.name,
            'description':item_t.description,
            })
    ctx = {'form': form, 'item_t': item_t}
    return render_to_response('des/item_type/modify_item_type.html', ctx, context_instance=RequestContext(request))

def delete_item_type(request, id_item_type):
    """
    Elimina un atributo del sistema.
    """
    item_t = ItemType.objects.get(id=id_item_type)
    if request.method == "POST":
        item_t.delete()
        return HttpResponseRedirect('/des/list_item_types/')
    if request.method == "GET":
        ctx = {'item_t':item_t}
        return render_to_response('des/item_type/delete_item_type.html', ctx, context_instance=RequestContext(request))

def assign_item_attribute(request, id_item_type):
    attr = Attribute.objects.all()
    item_t = ItemType.objects.get(id=id_item_type)
    ctx = {'item_t':item_t, 'attr':attr}
    return render_to_response('des/item_type/assign_item_attribute.html', ctx, context_instance=RequestContext(request))
    
def grant_attribute(request, id_item_type, id_attribute):
    item_t = ItemType.objects.get(id=id_item_type)
    attr = Attribute.objects.get(id=id_attribute)
    new_attr = False
    try:
        attr = item_t.attributes.get(id=id_attribute)
    except Attribute.DoesNotExist:
        new_attr = True      
    if new_attr:
        item_t.attributes.add(attr)
        item_t.save()
    ctx = {'item_t':item_t, 'attr':attr, 'valid':new_attr}
    return render_to_response('des/item_type/grant_attribute.html', ctx, context_instance=RequestContext(request))

def deny_attribute(request, id_item_type, id_attribute):
    item_t = ItemType.objects.get(id=id_item_type)
    attr = Attribute.objects.get(id=id_attribute)
    item_t.attributes.remove(attr)
    item_t.save()
    ctx = {'item_t':item_t, 'attr':attr}
    return render_to_response('des/item_type/deny_attribute.html', ctx, context_instance=RequestContext(request))

def visualize_item_type(request, id_item_type):
    """
    Despliega los campos de un tipo de item.
    """
    item_t = ItemType.objects.get(id=id_item_type)
    attrs = item_t.attributes.all()
    ctx = {'item_t': item_t, 'attrs':attrs}
    return render_to_response('des/item_type/visualize_item_type.html', ctx, context_instance=RequestContext(request))
