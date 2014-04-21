from django import forms
from django.contrib.auth.models import User
from adm.models import Permission, Role, Project

class add_user_form(forms.Form):
    username    = forms.CharField(label="Username", widget=forms.TextInput(), required=True)
    password    = forms.CharField(label="Contrasena", widget=forms.PasswordInput(render_value=False), required=True)
    firstName   = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    lastName    = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
    email       = forms.EmailField(label="E-mail", widget=forms.TextInput(), required=True)
    phonenum    = forms.CharField(label="Telefono", widget=forms.TextInput(), required=False)
    address     = forms.CharField(label="Direccion", widget=forms.TextInput(), required=False)
    observation = forms.CharField(label="Observacion", widget=forms.TextInput(), required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            if user.username==username:
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
        raise forms.ValidationError('El e-mail ya existe.')
    
class mod_user_form(forms.Form):
    passwd      = forms.CharField(label="Contrasena", widget=forms.PasswordInput(render_value=False), required=False)
    firstName   = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    lastName    = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
    email       = forms.EmailField(label="E-mail", widget=forms.TextInput(), required=True)
    phonenum    = forms.CharField(label="Telefono", widget=forms.TextInput(), required=False)
    address     = forms.CharField(label="Direccion", widget=forms.TextInput(), required=False)
    observation = forms.CharField(label="Observacion", widget=forms.TextInput(), required=False)
    
               
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user.email == email:
                return email
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('El E-mail ya existe.')

class add_role_form(forms.Form):
    """
    
    """
    name        = forms.CharField(label="Nombre", required=True)
    description = forms.CharField(label="Descripcion", required=False)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            role = Role.objects.get(name=name)
            if role.name == name:
                return name 
        except Role.DoesNotExist:
            return name
        raise forms.ValidationError('El nombre de rol ya existe.')    

class mod_role_form(forms.Form):
    """
    
    """
    name        = forms.CharField(label="Nombre", required=True)
    description = forms.CharField(label="Descripcion", required=False)
        
    def clean_nombre(self): 
        name = self.cleaned_data['name'] 
        try: 
            role = Role.objects.get(name=name) 
            if role.name == name:
                return name 
        except Role.DoesNotExist:
            return name 
        raise forms.ValidationError('El nombre de rol ya existe.')

class add_project_form(forms.Form):
    """
    
    """
    name = forms.CharField(label="Nombre", required=True)
    description = forms.CharField(label="Descripcion", required=True)
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            project = Project.objects.get(name=name)
            if project.name == name:
                return name
        except Project.DoesNotExist:
            return name
        raise forms.ValidationError('El nombre de proyecto ya existe.')