from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm, ProfileForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from usuarios.models import User
from django.contrib.auth.decorators import login_required

def sign(request):
    if request.user.is_authenticated:
        return redirect('temario')
    else: 
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
                    return redirect("/temario/")
            else:
                    messages.add_message(request=request,level=messages.ERROR, message="No existen usuarios con esa contraseña.")
        
        elif request.method == "POST" and 'register' in request.POST:

            form2 = CreateUserForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')

            if form2.is_valid():
                form2.save()
                
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    auth.login(request, user)
                    return redirect("/temario/")

            elif User.objects.filter(username = username).first():
                context=messages.add_message(request=request,level=messages.ERROR, message="Ya existe un usuario con ese nombre de usuario.")
                return render(request, 'usuarios/register.html', {'loginform':form1, 'registerform':form2,'context':context})
            
            elif User.objects.filter(email = email).first():
                context=messages.add_message(request=request,level=messages.ERROR, message="Ya existe un usuario con ese email.")
                return render(request, 'usuarios/register.html', {'loginform':form1, 'registerform':form2,'context':context})

            elif password != password2:
                    context=messages.add_message(request=request,level=messages.ERROR, message="Las contraseñas no coinciden.")
                    return render(request, 'usuarios/register.html', {'loginform':form1, 'registerform':form2,'context':context})

            elif len(password) < 8:
                    context=messages.add_message(request=request,level=messages.ERROR, message="La contraseña es muy corta. Debe contener al menos 8 caracteres.")
                    return render(request, 'usuarios/register.html', {'loginform':form1, 'registerform':form2,'context':context})
                

            else:
                context=messages.add_message(request=request,level=messages.ERROR, message="Ya hay un usuario registrado con ese nombre de ususario y/o email.")
                return render(request, 'usuarios/register.html', {'loginform':form1, 'registerform':form2,'context':context})
        else:
            
            return render(request, 'usuarios/sign.html', {'loginform':form1, 'registerform':form2})
        
        return render(request, 'usuarios/sign.html', {'loginform':form1, 'registerform':form2})


@login_required(login_url="sign")
def perfil(request):
    return render(request, 'usuarios/perfil.html')

@login_required(login_url="sign")
def editarPerfil(request):
    user=request.user.username
    profile=User.objects.get(username=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile.nombre = form.cleaned_data.get('nombre')
            profile.email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 != password2:
                context=messages.add_message(request=request,level=messages.ERROR, message="Las contraseñas no coinciden.")
                return render(request, 'usuarios/editarPerfil.html', {'form':form, 'context':context})
        

            if not password1 or not password2:
                profile.save()
                return redirect('perfil')
            else:
                profile.set_password(password1) 
                profile.save()
                return redirect('perfil')
        else:
             messages.add_message(request=request,level=messages.ERROR, message="Ya hay una cuenta con ese correo.")
    else:
        form = ProfileForm(instance=profile)
    
    context={'form':form}

    return render(request, 'usuarios/editarPerfil.html',context)

@login_required(login_url="sign")
def eliminarPerfil(request):
     user = request.user.username
     usuario = User.objects.get(username=user)
     usuario.delete()
     
     return redirect('sign')