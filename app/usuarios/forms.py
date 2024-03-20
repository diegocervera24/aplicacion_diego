from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from . models import User

# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'nombre', 'password1', 'password2']


# - Authenticate a user (Model Form)

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class ProfileForm(forms.ModelForm):
    password1 = forms.CharField(widget=PasswordInput(),required=False)
    password2 = forms.CharField(widget=PasswordInput(),required=False)
    
    class Meta:
        model = User
        fields = ['nombre','email', 'username', 'password1', 'password2']