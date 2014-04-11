#from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from adm.forms import addProductForm, addUserForm
from adm.models import producto, user

def add_product_view(request):
    if request.method == "POST": # POST
        form = addProductForm(request.POST)
        info = "Inicializando..."
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            p = producto()
            p.nombre = name
            p.descripcion = description
            p.status = True
            p.save() # Save information
            info = "Se ha almacenado satisfactoriamente."
        else:
            info = "informacion con datos incorrectos."
        form = addProductForm()
        ctx = {'form':form, 'information':info}
        return render_to_response('adm/addProduct.html', ctx, context_instance=RequestContext(request))
    else: # GET
        form = addProductForm()
        ctx = {'form':form}
        return render_to_response('adm/addProduct.html', ctx, context_instance=RequestContext(request))

# REAL VIEW

def add_user_view(request):
    if request.method == "POST": # POST
        form = addUserForm(request.POST)
        info = "Inicializando..."
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phonenum = form.cleaned_data['phonenum']
            direction = form.cleaned_data['direction']
            observation = form.cleaned_data['observation']
            p = user()
            p.username = username
            p.password = password
            p.email = email
            p.phonenum = phonenum
            p.direction = direction
            p.observation = observation
            p.status = True
            p.save() # Save information
            info = "Se ha almacenado satisfactoriamente."
        else:
            info = "informacion con datos incorrectos."
        form = addUserForm()
        ctx = {'form':form, 'information':info}
        return render_to_response('adm/addUser.html', ctx, context_instance=RequestContext(request))
    else: # GET
        form = addUserForm()
        ctx = {'form':form}
        return render_to_response('adm/addUser.html', ctx, context_instance=RequestContext(request))
