from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from usuarios.models import User
from oposicion.models import Oposicion, Temario, Prueba, Progreso, Formado_por
from django.core.files.uploadedfile import SimpleUploadedFile

class TestViews(TestCase):

    def setUp(self):
        self.client_nolog = Client() # Cliente no logueado
        self.client = Client() # Creamos un cliente que se encargará de realizar las peticiones a las distintas urls que probaremos.
        self.user = User.objects.create_user(nombre='Tester', username='testuser', email='tester@email.com', password='testpassword') # Creamos un usuario que asignaremos al cliente que realiza las peticiones.
        self.user2 = User.objects.create_user(nombre='Tester2', username='testuser2', email='tester2@email.com', password='testpassword') # Creamos un usuario que asignaremos al cliente que realiza las peticiones.
        self.client.login(username='testuser', password='testpassword') # Asignamos el usuario al cliente haciendo que comparta sus credenciales.

        #Declaramos las distintas urls que nos permiten acceder a las pantallas
        self.homepage_url = reverse('homepage')
        self.temario_url = reverse('temario') 
        self.mostrar_temario_url = reverse('mostrar_temario', args=[1]) #Accede al temario con id=1
        self.mostrar_temario2_url = reverse('mostrar_temario', args=[3]) #Accede al temario con id=1
        self.ver_pdf_url = reverse('ver_pdf', args=[10,"testuser/aisi2324-practica2.pdf"]) #Visualiza el temario con id=1 
        self.eliminarTemario_url = reverse('eliminarTemario', args=[10]) #Borra el temario con id=10
        self.eliminarTemario2_url = reverse('eliminarTemario', args=[12]) #Borra el temario con id=10
        self.pruebas_url = reverse('pruebas')
        self.mostrar_prueba_url = reverse('mostrar_prueba', args=[1]) #Muestra la prueba con oposicon id=1
        self.mostrar_prueba2_url = reverse('mostrar_prueba', args=[3]) #Muestra la prueba con oposicon id=1
        self.eliminarPrueba_url = reverse('eliminarPrueba', args=[10]) #Elimina la prueba con id=1
        self.eliminarPrueba2_url = reverse('eliminarPrueba', args=[12]) #Elimina la prueba con id=1
        self.realizarPrueba_url = reverse('realizarPrueba',args=["Prueba4_2"])
        self.realizarPrueba2_url = reverse('realizarPrueba',args=["Prueba_132"]) 
        self.progreso_url = reverse('progreso')
        self.progresoOposicion_url = reverse('progresoOposicion', args=[1]) #Muestra progreso de la oposicion con id=1


        self.oposicion = Oposicion.objects #Creamos una variable para acceder a la tabla oposicion
        self.opo1 = self.oposicion.create(id=1, NomOposicion="Oposicion1", OpoVisible=True)
        self.opo2 = self.oposicion.create(id=2, NomOposicion="Oposicion2", OpoVisible=True)
        self.opo3 = self.oposicion.create(id=3, NomOposicion="Oposicion3", OpoVisible=True)

        self.temario = Temario.objects #Creamos una variable para acceder a la tabla temario
        with open('C:/Users/DIEGO/Desktop/Informática/Cuarto/2º Cuatrimestre/AISI/aisi2324-practica2.pdf', 'rb') as file:
            archivo = SimpleUploadedFile('aisi2324-practica2.pdf', file.read())
        self.temario1 = self.temario.create(id=10, NomTemario="Temario1", NumPaginas=150, TemVisible=True, Archivo=archivo, NomUsuario_id=self.user.username, IdOposicion_id=1)
        self.temario2 = self.temario.create(id=11, NomTemario="Temario2", NumPaginas=98, TemVisible=True, Archivo=archivo, NomUsuario_id=self.user.username, IdOposicion_id=1)
        self.temario3 = self.temario.create(id=12, NomTemario="Temario1", NumPaginas=136, TemVisible=True, Archivo=archivo, NomUsuario_id=self.user2.username, IdOposicion_id=1)
        self.temario4 = self.temario.create(id=13, NomTemario="Temario1", NumPaginas=142, TemVisible=True, Archivo=archivo, NomUsuario_id=self.user.username, IdOposicion_id=2)

        self.prueba = Prueba.objects #Creamos una variable para acceder a la tabla prueba
        self.prueba1 = self.prueba.create(id=10, NomPrueba="Prueba1", NumPreguntas=15)
        self.prueba2 = self.prueba.create(id=11, NomPrueba="Prueba2", NumPreguntas=8)
        self.prueba3 = self.prueba.create(id=12, NomPrueba="Prueba1", NumPreguntas=12)
        self.prueba4 = self.prueba.create(id=13, NomPrueba="Prueba3", NumPreguntas=30)

        self.progreso = Progreso.objects #Creamos una variable para acceder a la tabla progreso
        self.progreso1 = self.progreso.create(id=1, Nota=10, PregAcertadas=15, PregFalladas=0, PregBlanco=0, Tiempo=412, IdPrueba=self.prueba1)
        self.progreso2 = self.progreso.create(id=2, Nota=8, PregAcertadas=7, PregFalladas=0, PregBlanco=1, Tiempo=382, IdPrueba=self.prueba2)
        self.progreso3 = self.progreso.create(id=3, Nota=9, PregAcertadas=0, PregFalladas=0, PregBlanco=0, Tiempo=435, IdPrueba=self.prueba3)
        self.progreso4 = self.progreso.create(id=4, Nota=5, PregAcertadas=15, PregFalladas=0, PregBlanco=15, Tiempo=662, IdPrueba=self.prueba4)
        
        self.formado_por = Formado_por.objects #Creamos una variable para acceder a la tabla formado_por
        self.formado_por1 = self.formado_por.create(id=10, IdTemario_id=10, IdPrueba_id=10)
        self.formado_por2 = self.formado_por.create(id=11, IdTemario_id=11, IdPrueba_id=10)
        self.formado_por3 = self.formado_por.create(id=12, IdTemario_id=11, IdPrueba_id=11)
        self.formado_por4 = self.formado_por.create(id=13, IdTemario_id=12, IdPrueba_id=12)
        self.formado_por5 = self.formado_por.create(id=14, IdTemario_id=13, IdPrueba_id=13)

    def test_homepage_get(self):
        response = self.client_nolog.get(self.homepage_url)
        
        # Comprobamos que la petición GET renderiza la pantalla principal con la devolución de un código 200.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/index.html')

    def test_temario_get(self):
        response = self.client.get(self.temario_url)

        # Comprobamos que la petición GET renderiza la pantalla de temario con la devolución de un código 200.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/temario.html')

    def test_temario_añadir_valido_sin_oposicion_post(self):
        with open('C:/Users/DIEGO/Desktop/Informática/Cuarto/2º Cuatrimestre/AISI/aisi2324-practica2.pdf', 'rb') as file:
            archivo = SimpleUploadedFile('aisi2324-practica2.pdf', file.read())

        #Añadimos un temario
        response = self.client.post(self.temario_url,{
            'NomTemario':'Temario3',
            'NumPaginas': 120,
            'Archivo': archivo,
            'IdOposicion': 3
        })

        # Comprobamos que la aplicación le redirige a la pantalla temario ('/temario/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/temario/')

        # Comprobamos que el usuario tiene 4 temarios
        temario_count = self.temario.filter(NomUsuario_id=self.user.username).count()
        self.assertEqual(temario_count, 4)

        # Comprobamos que hay tres oposiciones en temario
        oposicion_count = self.temario.filter(NomUsuario_id=self.user.username).values_list('IdOposicion_id').distinct().count()
        self.assertEqual(oposicion_count, 3)

    def test_temario_añadir_valido_oposicion_existente_post(self):
        with open('C:/Users/DIEGO/Desktop/Informática/Cuarto/2º Cuatrimestre/AISI/aisi2324-practica2.pdf', 'rb') as file:
            archivo = SimpleUploadedFile('aisi2324-practica2.pdf', file.read())

        #Añadimos un temario
        response = self.client.post(self.temario_url,{
            'NomTemario':'Temario3',
            'NumPaginas': 120,
            'Archivo': archivo,
            'IdOposicion': 1
        })

        # Comprobamos que la aplicación le redirige a la pantalla temario ('/temario/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/temario/')

        # Comprobamos que el usuario tiene 4 temarios
        temario_count = self.temario.filter(NomUsuario_id=self.user.username).count()
        self.assertEqual(temario_count, 4)

        # Comprobamos que hay tres oposiciones en temario
        oposicion_count = self.temario.filter(NomUsuario_id=self.user.username).values_list('IdOposicion_id').distinct().count()
        self.assertEqual(oposicion_count, 2)

    def test_temario_añadir_nombre_invalido_post(self):
        with open('C:/Users/DIEGO/Desktop/Informática/Cuarto/2º Cuatrimestre/AISI/aisi2324-practica2.pdf', 'rb') as file:
            archivo = SimpleUploadedFile('aisi2324-practica2.pdf', file.read())

        #Añadimos un temario
        response = self.client.post(self.temario_url,{
            'NomTemario':'Temario1',
            'NumPaginas': 112,
            'Archivo': archivo,
            'IdOposicion': 1
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/temario.html')
        self.assertContains(response, "Ya existe un fichero con el mismo nombre.")

        # Comprobamos que no se añadieron temarios
        temario_count = self.temario.filter(NomUsuario_id=self.user.username).count()
        self.assertEqual(temario_count, 3)
    
    def test_mostrar_temario_get(self):
        response = self.client.get(self.mostrar_temario_url)

        # Comprobamos que la petición GET renderiza la pantalla de temario con la devolución de un código 200.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/mostrar_temario.html')

        # Comprobamos que el usuario tiene 2 temarios
        temario_count = self.temario.filter(NomUsuario_id=self.user.username, TemVisible=True, IdOposicion=1).count()
        self.assertEqual(temario_count, 2)


    def test_mostrar_temario_sin_get(self):
        response = self.client.get(self.mostrar_temario2_url)

        # Comprobamos que la petición GET renderiza la pantalla de temario con la devolución de un código 200.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/mostrar_temario.html')
        self.assertContains(response, "No hay temario subido.")

    def test_ver_pdf_get(self):
        with open('C:/Users/DIEGO/Desktop/Informática/Cuarto/2º Cuatrimestre/AISI/aisi2324-practica2.pdf', 'rb') as file:
            archivo = SimpleUploadedFile('aisi2324-practica2.pdf', file.read())
        response = self.client.post(self.temario_url,{
            'NomTemario':'Temario4',
            'NumPaginas': 112,
            'Archivo': archivo,
            'IdOposicion': 1
        })
        arch = self.temario.filter(id=4).values_list("Archivo", flat=True)
        archivo_completo = arch[0]
        self.ver_pdf_url1 = reverse('ver_pdf', args=[3,archivo_completo]) #Visualiza el temario con id=1 
        response = self.client.get(self.ver_pdf_url1)
        

        # Comprobamos que la petición GET renderiza la pantalla del pdf
        self.assertEqual(response.status_code, 200)

    def test_eliminar_temario_get(self):
        response = self.client.get(self.eliminarTemario_url)

        # Comprobamos que la aplicación le redirige a la pantalla temario ('/temario/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/temario/')

        temario_count = self.temario.filter(NomUsuario_id=self.user.username,TemVisible=True).count()
        self.assertEqual(temario_count, 2)

    def test_eliminar_temario_invalido_get(self):
        response = self.client.get(self.eliminarTemario2_url)

        # Comprobamos que la aplicación le redirige a la pantalla temario ('/temario/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/temario/')

        # Comprobamos que el usuario dos sigue teniendo 1 temario y no se borró
        temario_count = self.temario.filter(NomUsuario_id=self.user2.username,TemVisible=True).count()
        self.assertEqual(temario_count, 1)

    def test_pruebas_get(self):
        response = self.client.get(self.pruebas_url)

        # Comprobamos que la petición GET renderiza la pantalla de temario con la devolución de un código 200.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/pruebas.html')

    def test_prueba_añadir_valido_post(self):
        
        #Añadimos una prueba
        response = self.client.post(self.pruebas_url,{
            'NomPrueba':'Prueba4',
            'temarios': 10,
            'NumPreguntas': 12
        })

        # Comprobamos que la aplicación le redirige a la pantalla pruebas ('/pruebas/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pruebas/')

        # Comprobamos que ha creado correctamente la prueba
        prueba = self.prueba.filter(NomPrueba='Prueba4').count()
        self.assertEqual(prueba, 1)

        # Comprobamos que el usuario tiene 3 pruebas
        prueba_count = self.formado_por.prefetch_related('IdTemario','IdPrueba').filter(IdTemario__NomUsuario__username=self.user.username,IdPrueba__PruVisible=True).values_list('IdPrueba__id').distinct().count()
        self.assertEqual(prueba_count, 4)

    def test_prueba_añadir_invalido_post(self):
        
        #Añadimos una prueba
        response = self.client.post(self.pruebas_url,{
            'NomPrueba':'Prueba4',
            'temarios': [10,13],
            'NumPreguntas': 12
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/pruebas.html')
        self.assertContains(response, "El temario escogido tiene que ser de la misma oposición.")

        # Comprobamos que el usuario tiene 3 pruebas
        prueba_count = self.formado_por.prefetch_related('IdTemario','IdPrueba').filter(IdTemario__NomUsuario__username=self.user.username,IdPrueba__PruVisible=True).values_list('IdPrueba__id').distinct().count()
        self.assertEqual(prueba_count, 3)

    def test_mostrar_pruebas_get(self):
        response = self.client.get(self.mostrar_prueba_url)

        # Comprobamos que la petición GET renderiza la pantalla de mostrar pruebas con la devolución de un código 200.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/mostrar_prueba.html')

    def test_mostrar_pruebas_sin_get(self):
        response = self.client.get(self.mostrar_prueba2_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/mostrar_prueba.html')
        self.assertContains(response, "No hay pruebas creadas.")

    def test_eliminar_prueba_get(self):
        response = self.client.get(self.eliminarPrueba_url)

        # Comprobamos que la aplicación le redirige a la pantalla pruebas ('/pruebas/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pruebas/')

        prueba_count = self.formado_por.prefetch_related('IdTemario','IdPrueba').filter(IdTemario__NomUsuario__username=self.user.username,IdPrueba__PruVisible=True).values_list('IdPrueba__id').distinct().count()
        self.assertEqual(prueba_count, 2)

    def test_eliminar_prueba_invalida_get(self):
        response = self.client.get(self.eliminarPrueba2_url)

        # Comprobamos que la aplicación le redirige a la pantalla pruebas ('/pruebas/')
        # y que el código corresponde a una redirección (código 302).
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pruebas/')

        prueba_count = self.formado_por.prefetch_related('IdTemario','IdPrueba').filter(IdTemario__NomUsuario__username=self.user.username,IdPrueba__PruVisible=True).values_list('IdPrueba__id').distinct().count()
        self.assertEqual(prueba_count, 3)

    def test_realizar_prueba_get(self):
        #Añadimos una prueba
        response = self.client.post(self.pruebas_url,{
            'NomPrueba':'Prueba4',
            'temarios': 10,
            'NumPreguntas': 12
        })

        response = self.client.get(self.realizarPrueba_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/realizar_prueba.html')        

    def test_realizar_prueba_invalida_get(self):
        response = self.client.get(self.realizarPrueba2_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pruebas/')

    def test_progreso_get(self):
        response = self.client.get(self.progreso_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/progreso.html')
        self.assertContains(response, "Preguntas realizadas: 53")
        self.assertContains(response, "Nota media: 7.67")
        self.assertContains(response, "Tiempo medio empleado: 08:05")
        
        count_oposicion = Formado_por.objects.all().prefetch_related('IdTemario','IdPrueba','IdPrueba__progreso').filter(IdTemario__NomUsuario__username=self.user.username,IdPrueba__progreso__id__isnull=False).values_list('IdTemario__IdOposicion_id').distinct().count()
        self.assertEqual(count_oposicion, 2)

    def test_progreso_oposicion_get(self):
        response = self.client.get(self.progresoOposicion_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oposicion/progresoOposicion.html')
        self.assertContains(response, "Preguntas realizadas: 23")
        self.assertContains(response, "Nota media: 9.00")
        self.assertContains(response, "Tiempo medio empleado: 06:37")

        



