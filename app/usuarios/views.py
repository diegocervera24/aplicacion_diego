from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

def homepage(request):
    return render(request, 'usuarios/index.html')

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")


    context = {'registerform':form}

    return render(request, 'usuarios/register.html', context=context)

def login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")


    context = {'loginform':form}

    return render(request, 'usuarios/login.html', context=context)

def dashboard(request):
    return render(request, 'usuarios/dashboard.html')

def logout(request):

    auth.logout(request)

    return redirect("")

@login_required(login_url="login")
def dashboard(request):

    return render(request, 'usuarios/dashboard.html')