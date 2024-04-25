from django.test import TestCase
from django.urls import reverse, resolve
from usuarios.views import sign, perfil, editarPerfil, eliminarPerfil, logout


class TestUrls(TestCase):

    def test_registro_url_resolves(self):
        url = reverse('sign')
        self.assertEquals(resolve(url).func, sign)
    
    def test_perfil_url_resolves(self):
        url = reverse('perfil')
        self.assertEquals(resolve(url).func, perfil)

    def test_editarPerfil_url_resolves(self):
        url = reverse('editarPerfil')
        self.assertEquals(resolve(url).func, editarPerfil)
    
    def test_eliminarPerfil_url_resolves(self):
        url = reverse('eliminarPerfil')
        self.assertEquals(resolve(url).func, eliminarPerfil)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)
