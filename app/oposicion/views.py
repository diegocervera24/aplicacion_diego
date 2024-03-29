from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from PyPDF2 import PdfFileReader
from oposicion.models import Temario, Oposicion, Formado_por, Prueba, Progreso
from . forms import TemarioForm, ExamenForm, PruebaForm
import json, os
from django.conf import settings
from django.db.models import Value, CharField, F
from django.db.models.functions import Concat
from django.http import FileResponse
from datetime import datetime

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
    form = PruebaForm(request.POST)

    all_oposicion = Oposicion.objects.all().order_by('NomOposicion')
    all_pruebas = Formado_por.objects.prefetch_related('IdTemario','IdPrueba').filter(IdTemario__NomUsuario__username=user,IdPrueba__PruVisible=True).values_list('IdTemario__IdOposicion', flat=True).distinct()
    all_temario = Temario.objects.all().filter(NomUsuario=user, TemVisible=True).values_list('id','NomTemario','IdOposicion').order_by('IdOposicion')
    

    for pruebas in all_pruebas:
        oposicion = Oposicion.objects.get(id=pruebas)
        cantidad = Formado_por.objects.all().prefetch_related('IdTemario','IdPrueba').filter(IdTemario__IdOposicion=oposicion,IdTemario__NomUsuario__username=user,IdPrueba__PruVisible=True).values('IdPrueba').distinct().count()
        nombreOposiciones.append((oposicion.id, oposicion.NomOposicion, cantidad))
    

    if request.method == 'POST':
        if form.is_valid():
            oposicion = []
            temarios_seleccionados = form.cleaned_data['temarios']
            for temario in temarios_seleccionados:
                oposicion.append(temario.IdOposicion)
            
            if oposicion.count(oposicion[0]) == len(oposicion):
                prueba = form.save()
                json_file_path = os.path.join(settings.STATICFILES_DIRS[1], 'oposicion', 'examenes', f'{prueba.NomPrueba}_{prueba.id}.json')
                with open(json_file_path, 'w') as json_file:
                    json_file.write('')
            
                for temario in temarios_seleccionados:
                    Formado_por.objects.create(IdPrueba=prueba, IdTemario=temario)
            
            else:
                context=messages.add_message(request=request,level=messages.ERROR, message="El temario escogido tiene que ser de la misma oposición.")
                return render(request, 'oposicion/pruebas.html',{'all_oposicion':all_oposicion , 'all_temario':all_temario ,'all_pruebas':all_pruebas, 'nombreOposiciones':nombreOposiciones, 'form':form, 'context':context})

            
        return redirect('pruebas')
    
    return render(request, 'oposicion/pruebas.html',{'all_oposicion':all_oposicion , 'all_temario':all_temario ,'all_pruebas':all_pruebas, 'nombreOposiciones':nombreOposiciones, 'form':form})

@login_required(login_url="sign")
def mostrar_prueba(request, id):
    user=request.user.username
    oposicion = get_object_or_404(Oposicion, id=id)
    pruebas = Formado_por.objects.all().prefetch_related('IdTemario','IdPrueba').filter(IdTemario__IdOposicion=id,IdTemario__NomUsuario__username=user,IdPrueba__PruVisible=True).annotate(nombre_id=Concat(F('IdPrueba__NomPrueba'), Value('_'), F('IdPrueba__id'), output_field=CharField())).values_list('IdPrueba', 'IdPrueba__NomPrueba','nombre_id','IdPrueba__NumPreguntas').distinct()
    temario = Formado_por.objects.all().prefetch_related('IdTemario','IdPrueba').filter(IdTemario__IdOposicion=id,IdTemario__NomUsuario__username=user,IdPrueba__PruVisible=True).values_list('IdPrueba','IdTemario__NomTemario')


    return render(request, 'oposicion/mostrar_prueba.html', {'oposicion': oposicion,'pruebas': pruebas, 'temario':temario})

@login_required(login_url="sign")
def eliminarPrueba(request, id):
    elemento = get_object_or_404(Prueba, id=id)
    elemento.PruVisible = False
    elemento.save()

    return redirect ('pruebas')

@login_required(login_url="sign")
def realizarPrueba(request, titulo):
    _, id_prueba = titulo.split('_')
    hora_inicio = []

    ruta_archivo = os.path.join(settings.BASE_DIR, f'oposicion/static/oposicion/examenes/{titulo}.json')
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)
        examen_data = data.get('examen', {})
        preguntas = examen_data.get('preguntas', [])
        titulo = examen_data.get('titulo', [])

    hora_inicio = request.session.get('hora_inicio', [])
    hora_inicio.append(datetime.now().isoformat())
    request.session['hora_inicio'] = hora_inicio
    
    print(hora_inicio)
    if request.method == 'POST':
        form = ExamenForm(request.POST, preguntas=preguntas)

        respuestas_correctas = {(pregunta['id'], pregunta['respuesta_correcta']) for pregunta in preguntas}
        
        if form.is_valid():
            puntaje, incorrectas, blanco, nota, acertadas, falladas,  blancas, respuestas = form.evaluar_respuestas(preguntas)
            hora_fin = datetime.now().isoformat()
            hora_inicio_dt = datetime.fromisoformat(hora_inicio[0])
            hora_fin_dt = datetime.fromisoformat(hora_fin)

            tiempo = (hora_fin_dt - hora_inicio_dt)

            minutos = int(tiempo.total_seconds() // 60)
            segundos = int(tiempo.total_seconds() % 60) - 1

            tiempo_total = f"{minutos:02d}:{segundos:02d}"
            tiempo_segundos = tiempo.total_seconds()
            del request.session['hora_inicio']
            
            Progreso.objects.create(Nota=nota, PregAcertadas=puntaje, PregFalladas=incorrectas, PregBlanco=blanco, Tiempo=tiempo_segundos, IdPrueba_id=id_prueba)

            return render(request, 'oposicion/revisar_prueba.html', {'form': form, 'preguntas': preguntas,'puntaje': puntaje,'incorrectas':incorrectas, 'blanco':blanco, 'nota':nota, 'respuestas_correctas':respuestas_correctas, 'acertadas':acertadas, 'falladas':falladas, 'blancas':blancas, 'respuestas':respuestas,'titulo':titulo, 'hora_inicio': hora_inicio, 'tiempo_total':tiempo_total})
    else:
        form = ExamenForm(preguntas=preguntas)

    return render(request, 'oposicion/realizar_prueba.html', {'form': form, 'preguntas': preguntas})

@login_required(login_url="sign")
def ver_pdf(request,id, path):
    temario = get_object_or_404(Temario, Archivo=path)
    file_path = temario.Archivo.path
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

@login_required(login_url="sign")
def progreso(request):
     return render(request, 'oposicion/progreso.html')