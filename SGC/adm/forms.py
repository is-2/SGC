# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import Group, User
from adm.models import Project

class AddUserForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(), required=True)
    password = forms.CharField(label=u"Contraseña", widget=forms.PasswordInput(render_value=False), required=True)
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(), required=True)
    telephone = forms.CharField(label=u"Teléfono", widget=forms.TextInput(), required=True)
    address = forms.CharField(label=u"Dirección", widget=forms.TextInput(), required=False)
    observation = forms.CharField(label=u"Observación", widget=forms.TextInput(), required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            if user.username == username:
                return username
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('El nombre de usuario ya existe.')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user.email == email:
                return email
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('El email ya existe.')
    
class ModUserForm(forms.Form):
    password = forms.CharField(label=u"Contraseña", widget=forms.PasswordInput(render_value=False), required=False)
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(), required=True)
    telephone = forms.CharField(label=u"Teléfono", widget=forms.TextInput(), required=True)
    address = forms.CharField(label=u"Dirección", widget=forms.TextInput(), required=False)
    observation = forms.CharField(label=u"Observación", widget=forms.TextInput(), required=False)
    
               
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user.email == email:
                return email
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('El E-mail ya existe.')
    
class CreateGroupForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput, required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            group = Group.objects.get(name=name)
            if group.name == name:
                return name
        except Group.DoesNotExist:
            return name
        raise forms.ValidationError('El Rol ya existe.')

class ModGroupForm(forms.Form):
    """
    
    """
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
        
    def clean_nombre(self): 
        name = self.cleaned_data['name'] 
        try: 
            group = Group.objects.get(name=name) 
            if group.name == name:
                return name 
        except Group.DoesNotExist:
            return name 
        raise forms.ValidationError('El nombre de rol ya existe.')

class CreateProjectForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            project = Project.objects.get(name=name)
            if project.name == name:
                return name
        except Project.DoesNotExist:
            return name
        raise forms.ValidationError('El nombre de proyecto ya existe.')
    
class ModifyProjectForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput, required=True)
    description = forms.CharField(label=u"Descripción", widget=forms.TextInput(), required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            project = Project.objects.get(name=name)
            if project.name == name:
                return name
        except Project.DoesNotExist:
            return name
        raise forms.ValidationError('El nombre de Proyecto ya existe.')

class CreatePhaseForm(forms.Form):
    """
    """
    name = forms.CharField(label="Nombre", required=True)
    