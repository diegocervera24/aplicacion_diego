from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class TestViews(TestCase):

    def setUp(self):
        self.client = Client() # Creamos un cliente que se encargará de realizar las peticiones a las distintas urls que probaremos.

        self.sign_url = reverse('sign') # Declaramos la url que nos permite acceder a la pantalla de login.
        self.perfil_url = reverse('perfil') # Declaramos la url que nos permite acceder a la pantalla de perfil.
        self.editarPerfil_url = reverse('editarPerfil') # Declaramos la url que nos permite acceder a la pantalla de editar perfil.
        self.eliminarPerfil_url = reverse('eliminarPerfil') # Declaramos la url que nos permite eliminar perfil.
        self.logout_url = reverse('logout') # Declaramos la url que nos permite hacer logout.

        self.User = get_user_model() # Creamos una variable para acceder a la tabla de usuarios de la BD de las pruebas.
        self.user = self.User.objects.create_user(username='paco', password='Abc123..', email='paco@email.com', nombre='Paco González') # Añadimos al usuario paco a la tabla de usuarios de la BD de las pruebas.

    def test_perform_login_GET(self):
        response = self.client.get(self.sign_url)

        # Comprobamos que la petición GET renderiza la pantalla de login con la devolución de un código 200.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/sign.html')
    
    def test_perform_login_invalido_POST(self):
        # El usuario pepe cubre el formulario de login sin estar registrado.
        response = self.client.post(self.sign_url,{
            'username': 'pepe',
            'password': 'abc123..',
            'login': 'login'
        })

        # Como el usuario NO existe en la BD, comprobamos que se vuelve a renderizar la pantalla actual (código 200)
        # y que se envía el mensaje correspondiente por pantalla.
        self.assertTemplateUsed(response, 'usuarios/sign.html')
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "No existen usuarios con esa contraseña.")
        
        # Comprobamos que efectivamente NO se ha autenticado al usuario.
        self.assertFalse('_auth_user_id' in self.client.session)


    def test_perform_login_valido_POST(self):
        # El usuario paco cubre el formulario de login estando registrado.
        response = self.client.post(self.sign_url,{
            'username': 'paco',
            'password': 'Abc123..',
            'login': 'login'
        })

        # Como el usuario SÍ existe en la BD, comprobamos que la aplicación le redirige a la pantalla temario ('/temario/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/temario/')

        # Comprobamos que efectivamente SÍ se ha autenticado al usuario.
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_registro_valido_POST(self):
        # El usuario pepe cubre el formulario de registro correctamente.
        response = self.client.post(self.sign_url, {
            'nombre': 'Pepe López',
            'username': 'pepe',
            'email': 'pepe@udc.es',
            'password1': 'Abc123..',
            'password2': 'Abc123..',
            'register': 'register'
        })

        # Como el usuario NO existe en la BD y los datos son correctos, comprobamos que la aplicación le redirige a la pantalla principal ('/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/temario/')

        # Accedemos a la BD para comprobar que se ha registrado al usuario con el nombre y email correspondientes.
        user = self.User.objects.get(username='pepe')
        self.assertEqual(user.email, 'pepe@udc.es')

        # Comprobamos que además de resgistrar al usuario, también se le ha autenticado.
        self.assertTrue('_auth_user_id' in self.client.session)  

    def test_registro_datos_invalidos_POST(self):
        # El usuario pepe cubre el formulario de registro.
        response = self.client.post(self.sign_url, {
            'nombre': 'Pepe López',
            'username': 'pepe',
            'email': 'pepe@udc.es',
            'password1': 'Abc123.', # La contraseña es incorrecta por no cumplir con los 8 caracteres mínimos.
            'password2': 'Abc123.',
            'register': 'register'
        })

        # Como los datos del usuario que se quiere registrar son incorrectos, comprobamos que se vuelve a renderizar la pantalla actual (código 200)
        # y que se envía el mensaje correspondiente por pantalla.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/register.html')
        self.assertContains(response, "La contraseña es muy corta. Debe contener al menos 8 caracteres.")

        # Accedemos a la BD para comprobar que NO se ha registrado al usuario.
        with self.assertRaises(self.User.DoesNotExist):
            self.User.objects.get(username='pepe')

        # Comprobamos que, por supuesto, tampoco se le ha autenticado.
        self.assertFalse('_auth_user_id' in self.client.session)  

    def test_registro_usuario_existente_POST(self):
        # El usuario paco cubre el formulario de registro estando ya registrado anteriormente.
        response = self.client.post(self.sign_url, {
            'nombre': 'Paco González',
            'username': 'paco',
            'email': 'paco@email.es',
            'password1': 'Abc123..',
            'password2': 'Abc123..',
            'register': 'register'
        })

        # Como el usuario que se quiere registrar ya existe, comprobamos que se vuelve a renderizar la pantalla actual (código 200)
        # y que se envía el mensaje correspondiente por pantalla.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/register.html')
        self.assertContains(response, "Ya existe un usuario con ese nombre de usuario.")

        # Accedemos a la BD para comprobar que sigue existiendo un único usuario con ese nombre.
        user_count = self.User.objects.filter(username='paco').count()
        self.assertEqual(user_count, 1)

        # Comprobamos que, por supuesto, tampoco se le ha autenticado.
        self.assertFalse('_auth_user_id' in self.client.session)
    
    def test_registro_usuario_email_POST(self):
        # El usuario paco cubre el formulario de registro estando ya el email registrado.
        response = self.client.post(self.sign_url, {
            'nombre': 'Paco González',
            'username': 'paquito',
            'email': 'paco@email.com',
            'password1': 'Abc123..',
            'password2': 'Abc123..',
            'register': 'register'
        })

        # Como el email con el que el usuario se quiere registrar ya existe, comprobamos que se vuelve a renderizar la pantalla actual (código 200)
        # y que se envía el mensaje correspondiente por pantalla.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/register.html')
        self.assertContains(response, "Ya existe un usuario con ese email.")

        # Accedemos a la BD para comprobar que sigue existiendo un único usuario con ese nombre.
        user_count = self.User.objects.filter(username='paco').count()
        self.assertEqual(user_count, 1)

        # Comprobamos que, por supuesto, tampoco se le ha autenticado.
        self.assertFalse('_auth_user_id' in self.client.session)
    
    def test_perform_logout(self):
        # El usuario hace login.
        self.client.post(self.sign_url,{
            'username': 'paco',
            'password': 'Abc123..',
            'login': 'login'
        })

        # Comprobamos que el usuario está autenticado.
        self.assertTrue('_auth_user_id' in self.client.session)    

        # El usuario hace logout.
        response = self.client.get(self.logout_url)

        # Como el usuario acaba de hacer logout, comprobamos que la aplicación le redirige a la pantalla principal ('/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Comprobamos que el usuario ya NO está autenticado.
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_perform_perfil_GET(self):
        # El usuario hace login.
        self.client.post(self.sign_url,{
            'username': 'paco',
            'password': 'Abc123..',
            'login': 'login'
        })

        # Comprobamos que el usuario está autenticado.
        self.assertTrue('_auth_user_id' in self.client.session)

        response = self.client.get(self.perfil_url)

        # Comprobamos que la petición GET renderiza la pantalla de login con la devolución de un código 200.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/perfil.html')

    def test_perform_eliminarPerfil_GET(self):
        # Accedemos a la BD para comprobar existe un usuario con ese nombre.
        user_count = self.User.objects.filter(username='paco').count()
        self.assertEqual(user_count, 1)

        # El usuario hace login.
        self.client.post(self.sign_url,{
            'username': 'paco',
            'password': 'Abc123..',
            'login': 'login'
        })

        # Comprobamos que el usuario está autenticado.
        self.assertTrue('_auth_user_id' in self.client.session)

        response = self.client.get(self.eliminarPerfil_url)

         # Como el usuario acaba de eliminar la cuenta, comprobamos que la aplicación le redirige a la pantalla principal ('/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/sign/')

        # Comprobamos que el usuario ya NO está autenticado.
        self.assertFalse('_auth_user_id' in self.client.session)

        # Accedemos a la BD para comprobar que ya no existen usuarios con ese nombre.
        user_count = self.User.objects.filter(username='paco').count()
        self.assertEqual(user_count, 0)

    def test_perform_editarPerfil_GET(self):
        # El usuario hace login.
        self.client.post(self.sign_url,{
            'username': 'paco',
            'password': 'Abc123..',
            'login': 'login'
        })
        
        # Comprobamos que el usuario está autenticado.
        self.assertTrue('_auth_user_id' in self.client.session)

        response = self.client.get(self.editarPerfil_url)

        # Comprobamos que la petición GET renderiza la pantalla de editarPerfil con la devolución de un código 200.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/editarPerfil.html')
    
    def test_perform_perfil_eliminarPerfil_editarPerfil_GET_invalid(self):

        response = self.client.get(self.perfil_url)

        # Comprobamos que la petición GET renderiza la pantalla de editarPerfil con la devolución de un código 200.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/sign/?next=/perfil/')

        response = self.client.get(self.eliminarPerfil_url)

        # Comprobamos que la petición GET renderiza la pantalla de editarPerfil con la devolución de un código 200.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/sign/?next=/perfil/eliminar')
        

        response = self.client.get(self.editarPerfil_url)

        # Comprobamos que la petición GET renderiza la pantalla de editarPerfil con la devolución de un código 200.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/sign/?next=/perfil/editar')
        
        
