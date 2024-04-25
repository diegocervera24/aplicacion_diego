from django.test import TestCase
from usuarios.models import User

class TestModels(TestCase):

    def setUp(self):
        self.usuario = User.objects # Creamos una variable para acceder a la tabla de usuarios de la BD de las pruebas.

    def test_Usuarios(self):
        nFilas = len(self.usuario.all()) 
        self.assertEqual(nFilas, 0) # Comprobamos que inicialmente la tabla está vacía.

        self.usuario.create(username="pepe", email="pepe@email.com", nombre="Pepe López", is_admin=True) # Creamos al usuario Pepe
        user_luis = self.usuario.create(username="luis", email="luis@email.com", nombre="Luis García") # Creamos al usuario Luis

        nFilas = len(self.usuario.all())
        self.assertEqual(nFilas, 2) # Comprobamos que la tabla tiene ahora dos filas.

        user_luis.delete() # Borramos al usuario Luis

        nFilas = len(self.usuario.all())
        self.assertEqual(nFilas, 1) # Comprobamos que la tabla tiene ahora una fila.

        admins = self.usuario.filter(is_admin=True).count() 
        self.assertEqual(admins, 1) # Comprobamos que hay solo 1 admin