from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

def homepage(request):
    return render(request, 'usuarios/index.html')

def sign(request):

    form1 = LoginForm()
    form2 = CreateUserForm()

    if request.method == 'POST' and 'login' in request.POST:

        form1 = LoginForm(request, data=request.POST)

        if form1.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    elif request.method == "POST" and 'register' in request.POST:

        form2 = CreateUserForm(request.POST)

        if form2.is_valid():
            form2.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    else:
        return render(request, 'usuarios/sign.html', {'loginform':form1, 'registerform':form2})
    
    return render(request, 'usuarios/sign.html', {'loginform':form1, 'registerform':form2})

    

def dashboard(request):
    return render(request, 'usuarios/dashboard.html')

def logout(request):

    auth.logout(request)

    return redirect("")

@login_required(login_url="sign")
def dashboard(request):

    return render(request, 'usuarios/dashboard.html')