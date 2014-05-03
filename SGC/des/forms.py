# -*- coding: utf-8 -*-
from django import forms
from des.models import AttributeType, Attribute, ItemType
import datetime

class CreateAttributeTypeForm(forms.Form):
    CHOICES = (
             (0, "Numerico"),
             (1, "Cadena"),
             (2, "Booleano"),
             (3, "Fecha"),
    )
    
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    choice = forms.ChoiceField(label='Tipo', widget=forms.RadioSelect(), choices=CHOICES, required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            attribute_type = AttributeType.objects.get(name=name)
            if attribute_type.name == name:
                return name
        except AttributeType.DoesNotExist:
            return name
        raise forms.ValidationError('El tipo de atributo ya existe.')

class AssignIntegerForm(forms.Form):
    attr_int = forms.IntegerField(label="Numero", widget=forms.NumberInput(), required=True)
    
class AssignStringForm(forms.Form):
    attr_str = forms.CharField(label="Cadena", widget=forms.TextInput, required=True)
    
class AssignBooleanForm(forms.Form):
    attr_bool = forms.BooleanField(label="Booleano", required=True)
    
class AssignDateForm(forms.Form):
    attr_date = forms.DateField(label="Fecha", widget=forms.DateInput(), required=True, initial=datetime.date.today)
    
class ModifyAttributeTypeForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            attribute_type = AttributeType.objects.get(name=name)
            if attribute_type.name == name:
                return name
        except AttributeType.DoesNotExist:
            return name
        raise forms.ValidationError('El tipo de atributo ya existe.')
    
class CreateAttributeForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
class ModifyAttributeForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            attribute = Attribute.objects.get(name=name)
            if attribute.name == name:
                return name
        except Attribute.DoesNotExist:
            return name
        raise forms.ValidationError('El atributo ya existe.')
    
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