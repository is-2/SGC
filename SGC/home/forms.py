from django import forms
from django.contrib.auth.models import User, Group

class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput, required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(render_value=False), required=True)
    
class SignUpForm(forms.Form):
    username    = forms.CharField(label="username", widget=forms.TextInput, required=True)
    password    = forms.CharField(label="password", widget=forms.PasswordInput(render_value=False), required=True)
    email       = forms.EmailField(label="email", widget=forms.TextInput, required=True)
    telephone   = forms.CharField(label="telefono", widget=forms.TextInput, required=True)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            if user.username==username:
                return username
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username ya existe.')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user.email == email:
                return email
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya existe.')
    

    