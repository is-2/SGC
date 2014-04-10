from django import forms

# TEST FORMS

class addProductForm(forms.Form):
    name        = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.TextInput())
    def clean(self):
        return self.cleaned_data

### REAL FORMS

class addUserForm(forms.Form):
    username    = forms.CharField(widget=forms.TextInput())
    password    = forms.CharField(widget=forms.TextInput())
    # status missing
    email       = forms.CharField(widget=forms.TextInput())
    phonenum    = forms.CharField(widget=forms.TextInput())
    direction   = forms.CharField(widget=forms.TextInput())
    observation = forms.CharField(widget=forms.Textarea())
    def clean(self):
        return self.cleaned_data