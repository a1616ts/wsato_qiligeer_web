from django.forms import ModelForm
from vm.models import Domains
from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField()

class DomainForm(ModelForm):
    class Meta:
        model = Domains
        fields = ('name', 'os', 'size', 'ram', 'vcpus')
