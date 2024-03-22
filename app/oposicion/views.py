from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from PyPDF2 import PdfFileReader
from oposicion.models import Temario, Oposicion
from . forms import TemarioForm

def homepage(request):
     if request.user.is_authenticated:
        return redirect('temario')
     else:
        return render(request, 'oposicion/index.html')

@login_required(login_url="sign")
def temario(request):
    nombreOposiciones = []
    user=request.user.username
    form = TemarioForm(request.POST, request.FILES)
    all_oposicion = Oposicion.objects.all().order_by('NomOposicion')
    all_temario = Temario.objects.all().prefetch_related('NomUsuario','IdOposicion').filter(NomUsuario__username=user,TemVisible=True).values_list('IdOposicion', flat=True).distinct()

    for temario in all_temario:
        oposicion = Oposicion.objects.get(id=temario)
        nombreOposiciones.append((oposicion.id, oposicion.NomOposicion))

    if request.method == 'POST':
        if request.FILES['Archivo'].name.endswith('.pdf'):
            pdf_file = request.FILES['Archivo']
            pdf_reader = PdfFileReader(pdf_file)
            num_paginas = pdf_reader.numPages
            if form.is_valid():
                temario = form.save(commit=False)
                temario.NumPaginas = num_paginas
                temario.NomUsuario = request.user
                temario.Archivo = request.FILES['Archivo']
                temario.save()
                return redirect('temario')
        else:
            context=messages.add_message(request=request,level=messages.ERROR, message="Solo se permiten subir archivos en formato pdf.")
            return render(request, 'oposicion/temario.html',{'nombreOposiciones':nombreOposiciones, 'all_oposicion':all_oposicion, 'form':form,'context':context})
            
    
    return render(request, 'oposicion/temario.html',{'nombreOposiciones':nombreOposiciones, 'all_oposicion':all_oposicion, 'form':form})


@login_required(login_url="sign")
def mostrar_temario(request, id):
    user=request.user.username
    oposicion = get_object_or_404(Oposicion, id=id)
    temarios = Temario.objects.filter(IdOposicion=id,NomUsuario=user,TemVisible=True)
    
    return render(request, 'oposicion/mostrar_temario.html', {'oposicion': oposicion,'temarios': temarios})

@login_required(login_url="sign")
def eliminarTemario(request, id):
    elemento = get_object_or_404(Temario, id=id)
    elemento.TemVisible = False
    elemento.save()
    print(elemento.id)
    return redirect ('temario')


def logout(request):

    auth.logout(request)
    return redirect("/")