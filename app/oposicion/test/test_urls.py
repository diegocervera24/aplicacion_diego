from django.test import TestCase
from django.urls import reverse, resolve
from oposicion.views import *

class TestUrls(TestCase):

    def test_homepage_url_resolves(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)
    
    def test_temario_url_resolves(self):
        url = reverse('temario')
        self.assertEquals(resolve(url).func, temario)
    
    def test_mostrar_temario_url_resolves(self):
        url = reverse('mostrar_temario', args=[1])
        self.assertEquals(resolve(url).func, mostrar_temario)

    def test_ver_pdf_url_resolves(self):
        url = reverse('ver_pdf', args=[1,1])
        self.assertEquals(resolve(url).func, ver_pdf)

    def test_eliminarTemario_url_resolves(self):
        url = reverse('eliminarTemario', args=[1])
        self.assertEquals(resolve(url).func, eliminarTemario)

    def test_pruebas_url_resolves(self):
        url = reverse('pruebas')
        self.assertEquals(resolve(url).func, pruebas)

    def test_mostrar_prueba_url_resolves(self):
        url = reverse('mostrar_prueba', args=[1])
        self.assertEquals(resolve(url).func, mostrar_prueba)

    def test_eliminarPrueba_url_resolves(self):
        url = reverse('eliminarPrueba', args=[1])
        self.assertEquals(resolve(url).func, eliminarPrueba)
    
    def test_realizarPrueba_url_resolves(self):
        url = reverse('realizarPrueba', args=[1])
        self.assertEquals(resolve(url).func, realizarPrueba)
    
    def test_progreso_url_resolves(self):
        url = reverse('progreso')
        self.assertEquals(resolve(url).func, progreso)
    
    def test_progresoOposicion_url_resolves(self):
        url = reverse('progresoOposicion', args=[1])
        self.assertEquals(resolve(url).func, progresoOposicion)
