from django import forms
from django.contrib.auth.models import User

class addUserForm(forms.Form):
    username    = forms.CharField(label="username", widget=forms.TextInput(), required=True)
    password    = forms.CharField(label="password", widget=forms.PasswordInput(render_value=False), required=True)
    firstName   = forms.CharField(label="firstName", widget=forms.TextInput(), required=True)
    lastName    = forms.CharField(label="lastName", widget=forms.TextInput(), required=True)
    email       = forms.EmailField(label="email", widget=forms.TextInput(), required=True)
    phonenum    = forms.CharField(label="phonenum", widget=forms.TextInput(), required=False)
    direction   = forms.CharField(label="direction", widget=forms.TextInput(), required=False)
    observation = forms.CharField(label="observation", widget=forms.TextInput(), required=False)

    def clean_username(self):
        username = self.cleanead_data['username']
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
    
class ModUserForm(forms.Form):
  
    firstName   = forms.CharField(label="firstName", widget=forms.TextInput(), required=True)
    lastName    = forms.CharField(label="lastName", widget=forms.TextInput(), required=True)
    email       = forms.EmailField(label="email", widget=forms.TextInput(), required=True)
    phonenum    = forms.CharField(label="phonenum", widget=forms.TextInput(), required=False)
    direction   = forms.CharField(label="direction", widget=forms.TextInput(), required=False)
    observation = forms.CharField(label="observation", widget=forms.TextInput(), required=False)
    
               
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user.email == email:
                return email
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('El e-mail ya existe.')
    