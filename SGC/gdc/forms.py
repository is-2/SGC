# -*- coding: utf-8 -*-
from django import forms
# Custom imports
from models import ModificationRequest

class CreateModificationRequestForm(forms.Form):
    title = forms.CharField(label=u'Titulo', widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u'Descripcion', widget=forms.Textarea(), required=True)
    
    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            mod_request = ModificationRequest.objects.get(title=title)
            if mod_request.title == title:
                return title
        except ModificationRequest.DoesNotExist:
            return title
        raise forms.ValidationError('La peticion ya existe.')
    
class ModifyPendingItemForm(forms.Form):
    title = forms.CharField(label=u'Titulo', widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u'Descripcion', widget=forms.Textarea(), required=True)
    
    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            mod_request = ModificationRequest.objects.get(title=title)
            if mod_request.title == title:
                return title
        except ModificationRequest.DoesNotExist:
            return title
        raise forms.ValidationError('La peticion ya existe.')
    