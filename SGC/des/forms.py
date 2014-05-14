# -*- coding: utf-8 -*-
from django import forms
from des.models import AttributeType, Attribute, ItemType, Item
import datetime

CHOICES = (
               (0, "Numerico"),
               (1, "Cadena"),
               (2, "Booleano"),
               (3, "Fecha"),
)

class CreateAttributeTypeForm(forms.Form):
    
    
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    attr_type = forms.ChoiceField(label='Tipo', widget=forms.RadioSelect(), choices=CHOICES, required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            attribute_type = AttributeType.objects.get(name=name)
            if attribute_type.name == name:
                return name
        except AttributeType.DoesNotExist:
            return name
        raise forms.ValidationError('El Tipo de Atributo ya existe.')

class AssignIntegerForm(forms.Form):
    attr_int = forms.IntegerField(label="Numero", widget=forms.NumberInput(), required=True)
    
class AssignStringForm(forms.Form):
    attr_str = forms.CharField(label="Cadena", widget=forms.TextInput, required=True)
    
class AssignBooleanForm(forms.Form):
    attr_bool = forms.BooleanField(label="Booleano", required=True)
    
class AssignDateForm(forms.Form):
    attr_date = forms.DateField(label="Fecha", widget=forms.DateInput(), required=True, initial=datetime.date.today)
    
    
    
class ModifyAttributeTypeForm(forms.Form):
    """
    Formulario para modificar el Tipo de Atributo seleccionado.
    """
    name = forms.CharField(label=u"Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    attr_type = forms.ChoiceField(label='Tipo', widget=forms.RadioSelect(), choices=CHOICES, required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            attribute_type = AttributeType.objects.get(name=name)
            if attribute_type.name == name:
                return name
        except AttributeType.DoesNotExist:
            return name
        raise forms.ValidationError('El Tipo de Atributo ya existe.')

# NOT USED
class CreateAttributeForm(forms.Form):
    name = forms.CharField(label=u"Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)

# NOT USED
class ModifyAttributeForm(forms.Form):
    name = forms.CharField(label=u"Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            attribute = Attribute.objects.get(name=name)
            if attribute.name == name:
                return name
        except Attribute.DoesNotExist:
            return name
        raise forms.ValidationError('El Atributo ya existe.')
    
class CreateItemTypeForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            item_t = ItemType.objects.get(name=name)
            if item_t.name == name:
                return name
        except ItemType.DoesNotExist:
            return name
        raise forms.ValidationError('El tipo de item ya existe.')
    
class ModifyItemTypeForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            item_t = ItemType.objects.get(name=name)
            if item_t.name == name:
                return name
        except ItemType.DoesNotExist:
            return name
        raise forms.ValidationError('El tipo de item ya existe.')
    
class CreateItemForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            item = Item.objects.get(name=name)
            if item.name == name:
                return name
        except Item.DoesNotExist:
            return name
        raise forms.ValidationError('El Item ya existe.')
    
class ModifyItemForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            item = Item.objects.get(name=name)
            if item.name == name:
                return name
        except Item.DoesNotExist:
            return name
        raise forms.ValidationError('El Item ya existe.')
    
class CreateBaseLineForm(forms.Form):
    """
    """
    name = forms.CharField(label="Nombre", required=True)
    
class ModifyBaseLineForm(forms.Form):
    """
    """
    name = forms.CharField(label="Nombre", widget=forms.TextInput, required=True)
