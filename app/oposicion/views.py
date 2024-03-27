from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from PyPDF2 import PdfFileReader
from oposicion.models import Temario, Oposicion, Formado_por, Prueba
from . forms import TemarioForm, ExamenForm
import json, os
from django.conf import settings
from django.core.paginator import Paginator

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
        cantidad = Temario.objects.filter(NomUsuario__username=user,IdOposicion=temario,TemVisible=True).count()
        nombreOposiciones.append((oposicion.id, oposicion.NomOposicion, cantidad))

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
    print(temarios)
    
    return render(request, 'oposicion/mostrar_temario.html', {'oposicion': oposicion,'temarios': temarios})

@login_required(login_url="sign")
def eliminarTemario(request, id):
    elemento = get_object_or_404(Temario, id=id)
    elemento.TemVisible = False
    elemento.save()

    return redirect ('temario')

@login_required(login_url="sign")
def pruebas(request):
    nombreOposiciones = []
    user=request.user.username
    all_oposicion = Oposicion.objects.all().order_by('NomOposicion')
    all_pruebas = Formado_por.objects.prefetch_related('IdTemario','IdPrueba').filter(IdTemario__NomUsuario__username=user,IdPrueba__PruVisible=True).values_list('IdTemario__IdOposicion', flat=True).distinct()
    all_temario = Temario.objects.all().filter(NomUsuario=user, TemVisible=True).values_list('id','NomTemario','IdOposicion').order_by('IdOposicion')
    print(all_temario)
    for pruebas in all_pruebas:
        oposicion = Oposicion.objects.get(id=pruebas)
        nombreOposiciones.append((oposicion.id, oposicion.NomOposicion))

    return render(request, 'oposicion/pruebas.html',{'all_oposicion':all_oposicion , 'all_temario':all_temario ,'all_pruebas':all_pruebas, 'nombreOposiciones':nombreOposiciones})

@login_required(login_url="sign")
def mostrar_prueba(request, id):
    user=request.user.username
    oposicion = get_object_or_404(Oposicion, id=id)
    pruebas = Formado_por.objects.all().prefetch_related('IdTemario','IdPrueba').filter(IdTemario__IdOposicion=id,IdTemario__NomUsuario__username=user,IdPrueba__PruVisible=True).values_list('IdPrueba', 'IdPrueba__NomPrueba')
    
    return render(request, 'oposicion/mostrar_prueba.html', {'oposicion': oposicion,'pruebas': pruebas})

@login_required(login_url="sign")
def eliminarPrueba(request, id):
    elemento = get_object_or_404(Prueba, id=id)
    elemento.PruVisible = False
    elemento.save()

    return redirect ('pruebas')

@login_required(login_url="sign")
def realizarPrueba(request, titulo):


    ruta_archivo = os.path.join(settings.BASE_DIR, f'oposicion/static/oposicion/examenes/{titulo}.json')
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)
        examen_data = data.get('examen', {})
        preguntas = examen_data.get('preguntas', [])

    if request.method == 'POST':
        form = ExamenForm(request.POST, preguntas=preguntas)
        if form.is_valid():
            puntaje, incorrectas, blanco = form.evaluar_respuestas(preguntas)
            return render(request, 'oposicion/resultado_examen.html', {'puntaje': puntaje,'incorrectas':incorrectas, 'blanco':blanco})
    else:
        form = ExamenForm(preguntas=preguntas)

    return render(request, 'oposicion/realizar_prueba.html', {'form': form, 'preguntas': preguntas})
