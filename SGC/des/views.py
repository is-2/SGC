from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.contenttypes.models import ContentType
from des.models import AttributeType, NumericType, StringType, BooleanType, DateType
from des import forms
# Create your views here.
@login_required(login_url='/login/')
def list_attribute_types(request):
    """
    """
    attribute_types = AttributeType.objects.all()
    ctx = {'attribute_types':attribute_types}
    return render_to_response('des/attribute_type/list_attribute_types.html', ctx, context_instance=RequestContext(request))

def create_attribute_type(request):
    """
    """
    def numeric_type(value):
        return NumericType(value=value)
    
    def string_type(value):
        return StringType(value=value)
    
    def boolean_type(value):
        return BooleanType(value=value)
    
    def date_type(value):
        return DateType(value=value)
    
    type_selector = {'numeric' : numeric_type,
             'string' : string_type,
             'boolean' : boolean_type,
             'date' : date_type
             }
    
    form = forms.CreateAttributeTypeForm()
    if request.method == "POST":
        form = forms.CreateAttributeTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            value = form.cleaned_data['value']
            rel_type = form.cleaned_data['type']
            content_object = type_selector[rel_type](value=value)
            content_object.save()
            attr_type = AttributeType(name=name, description=description, content_object=content_object)
            attr_type.save()
            return HttpResponseRedirect('/des/list_attribute_types/')
        else:
            ctx = {'form':form}
            return render_to_response('des/attribute_type/create_attribute_type.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('des/attribute_type/create_attribute_type.html', ctx, context_instance=RequestContext(request))
