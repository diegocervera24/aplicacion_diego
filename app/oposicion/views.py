from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from PyPDF2 import PdfFileReader
from oposicion.models import Temario, Oposicion
from . forms import TemarioForm

def homepage(request):
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
        nombreOposiciones.append(oposicion.NomOposicion)

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
            return redirect('temario')
            
    
    return render(request, 'oposicion/temario.html',{'nombreOposiciones':nombreOposiciones, 'all_oposicion':all_oposicion, 'form':form})



def logout(request):

    auth.logout(request)
    return redirect("/")