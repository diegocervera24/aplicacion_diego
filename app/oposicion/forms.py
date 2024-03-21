from django import forms
from django.forms.widgets import TextInput
from . models import Temario

class TemarioForm(forms.ModelForm):
    
    class Meta:
        model = Temario
        fields = ['NomTemario','IdOposicion','Archivo']