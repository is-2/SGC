# -*- coding: utf-8 -*-
from django import forms
from des.models import AttributeType

class CreateAttributeTypeForm(forms.Form):
    TYPES = (
             ('numeric', "Numeric"),
             ('string', "string"),
             ('boolean', "boolean"),
             ('date', "date"),
    )
    
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    type = forms.ChoiceField(label='Tipo', widget=forms.RadioSelect(), choices=TYPES, required=True)
    value = forms.CharField(label=u"Valor", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            attr_type = AttributeType.objects.get(name=name)
            if attr_type.name == name:
                return name
        except AttributeType.DoesNotExist:
            return name
        raise forms.ValidationError('El tipo de atributo ya existe.')