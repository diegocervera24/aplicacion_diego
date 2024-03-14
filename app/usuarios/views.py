from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib import messages


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
        else:
                messages.add_message(request=request,level=messages.ERROR, message="No existen usuarios con esa contraseña.")
    
    elif request.method == "POST" and 'register' in request.POST:

        form2 = CreateUserForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if form2.is_valid():
            form2.save()
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
            
        elif password != password2:
                context=messages.add_message(request=request,level=messages.ERROR, message="Las contraseñas no coinciden.")
                return render(request, 'usuarios/register.html', {'loginform':form1, 'registerform':form2,'context':context})

        else:
            context=messages.add_message(request=request,level=messages.ERROR, message="Ya hay un usuario registrado con ese nombre de ususario y/o email.")
            return render(request, 'usuarios/register.html', {'loginform':form1, 'registerform':form2,'context':context})
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