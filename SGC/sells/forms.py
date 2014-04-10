from django import forms

class addProductForm(forms.Form):
    name        = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.TextInput())
    def clean(self):
        return self.cleaned_data


    