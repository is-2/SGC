from django import forms
from django.contrib.auth.models import User

class add_user_form(forms.Form):
    username    = forms.CharField(label="Username", widget=forms.TextInput(), required=True)
    password    = forms.CharField(label="Contrasena", widget=forms.PasswordInput(render_value=False), required=True)
    firstName   = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    lastName    = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
    email       = forms.EmailField(label="E-mail", widget=forms.TextInput(), required=True)
    phonenum    = forms.CharField(label="Telefono", widget=forms.TextInput(), required=False)
    address   = forms.CharField(label="Direccion", widget=forms.TextInput(), required=False)
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
    