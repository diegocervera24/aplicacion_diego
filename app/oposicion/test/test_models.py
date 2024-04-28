from django.test import TestCase
from oposicion.models import Oposicion, Temario, Prueba, Progreso, Formado_por
from django.db import IntegrityError

class TestModels(TestCase):

    def setUp(self):

        # Creamos una variable para acceder a la tabla de oposición de la BD de las pruebas.
        self.oposicion = Oposicion.objects 
        #Insertamos 3 oposiciones
        self.oposicion1 = self.oposicion.create(id=1, NomOposicion="Oposicion1", OpoVisible=True)
        self.oposicion2 = self.oposicion.create(id=2, NomOposicion="Oposicion2", OpoVisible=True)
        self.oposicion3 = self.oposicion.create(id=3, NomOposicion="Oposicion3", OpoVisible=True)
        
        # Creamos una variable para acceder a la tabla de temario de la BD de las pruebas.
        self.temario = Temario.objects
        #Insertamos 3 temarios
        self.temario1 = self.temario.create(id=1, NomTemario="Temario1", NumPaginas=150, TemVisible=True, Archivo="aisi2324-practica4.pdf", NomUsuario_id="pepe", IdOposicion_id=1)
        self.temario2 = self.temario.create(id=2, NomTemario="Temario2", NumPaginas=98, TemVisible=True, Archivo="aisi2324-practica3.pdf", NomUsuario_id="pepe", IdOposicion_id=2)
        self.temario3 = self.temario.create(id=3, NomTemario="Temario1", NumPaginas=135, TemVisible=True, Archivo="aisi2324-practica2.pdf", NomUsuario_id="luis", IdOposicion_id=3)

        # Creamos una variable para acceder a la tabla de prueba de la BD de las pruebas.
        self.prueba = Prueba.objects
        #Insertamos 3 pruebas
        self.prueba1 = self.prueba.create(id=1, NomPrueba="Prueba1", NumPreguntas=18, PruVisible=True)
        self.prueba2 = self.prueba.create(id=2, NomPrueba="Prueba2", NumPreguntas=30, PruVisible=True)
        self.prueba3 = self.prueba.create(id=3, NomPrueba="Prueba1", NumPreguntas=7, PruVisible=True)

        # Creamos una variable para acceder a la tabla de formado_por de la BD de las pruebas.
        self.progreso = Progreso.objects
        #Insertamos 3 progresos
        self.progreso1 = self.progreso.create(id=1, Nota=7.5, PregAcertadas=14, PregFalladas=2, PregBlanco=2, Tiempo=532, IdPrueba_id=1)
        self.progreso2 = self.progreso.create(id=2, Nota=10, PregAcertadas=30, PregFalladas=0, PregBlanco=0, Tiempo=662, IdPrueba_id=2)
        self.progreso3 = self.progreso.create(id=3, Nota=7, PregAcertadas=5, PregFalladas=2, PregBlanco=0, Tiempo=322, IdPrueba_id=3)

        # Creamos una variable para acceder a la tabla de formado_por de la BD de las pruebas.
        self.formado_por = Formado_por.objects
        #Insertamos 3 filas
        self.formado_por1 = self.formado_por.create(id=1, IdTemario_id=1, IdPrueba_id=1)
        self.formado_por2 = self.formado_por.create(id=2, IdTemario_id=2, IdPrueba_id=2)
        self.formado_por3 = self.formado_por.create(id=3, IdTemario_id=3, IdPrueba_id=3)


    def test_Oposicion(self):
        nFilas = len(self.oposicion.all())
        self.assertEqual(nFilas, 3) # Comprobamos que la tabla de oposicion tiene inicialmente 3 filas.
        
        self.oposicion2.delete()  # Borramos la fila correspondiente a la oposicion de id=2

        nFilas = len(self.oposicion.all())
        self.assertEqual(nFilas, 2) # Comprobamos que, al borrar una fila, la tabla de oposicion ahora tiene 2 filas.

        oposicion1 = self.oposicion.filter(id=1).count()
        self.assertEqual(oposicion1, 1) # Comprobamos que solo existe una oposicion con id=1
        with self.assertRaises(self.oposicion.model.DoesNotExist):
            self.oposicion.get(id=2) # Comprobamos que se produce un error si se busca una oposicion con id=2
        oposicion3 = self.oposicion.filter(id=3).count()
        self.assertEqual(oposicion3, 1) # Comprobamos que solo existe una oposicion con id=3

        with self.assertRaises(IntegrityError):
            # Comprobamos que se produce un error si se intenta insertar una oposicion con id ya existente.
            self.oposicion.create(id=1, NomOposicion="Oposicion4", OpoVisible=True)

    def test_Temario(self):
        nFilas = len(self.temario.all())
        self.assertEqual(nFilas, 3) # Comprobamos que la tabla de temario tiene inicialmente 3 filas.
        
        self.temario2.delete()  # Borramos la fila correspondiente al temario de id=2

        nFilas = len(self.temario.all())
        self.assertEqual(nFilas, 2) # Comprobamos que, al borrar una fila, la tabla de temario ahora tiene 2 filas.

        temario1 = self.temario.filter(id=1).count()
        self.assertEqual(temario1, 1) # Comprobamos que solo existe un temario con id=1
        with self.assertRaises(self.temario.model.DoesNotExist):
            self.temario.get(id=2) # Comprobamos que se produce un error si se busca un temario con id=2
        temario3 = self.temario.filter(id=3).count()
        self.assertEqual(temario3, 1) # Comprobamos que solo existe un temario con id=3

        with self.assertRaises(IntegrityError):
            # Comprobamos que se produce un error si se intenta insertar un temario con id ya existente.
            self.temario.create(id=1, NomTemario="Temario3", NumPaginas=132, TemVisible=True, Archivo="aisi2324-practica1.pdf", NomUsuario_id="pepe", IdOposicion_id=1)

    def test_Prueba(self):
        nFilas = len(self.prueba.all())
        self.assertEqual(nFilas, 3) # Comprobamos que la tabla de prueba tiene inicialmente 3 filas.
        
        self.prueba2.delete()  # Borramos la fila correspondiente a la prueba de id=2

        nFilas = len(self.prueba.all())
        self.assertEqual(nFilas, 2) # Comprobamos que, al borrar una fila, la tabla de prueba ahora tiene 2 filas.

        prueba1 = self.prueba.filter(id=1).count()
        self.assertEqual(prueba1, 1) # Comprobamos que solo existe una prueba con id=1
        with self.assertRaises(self.prueba.model.DoesNotExist):
            self.prueba.get(id=2) # Comprobamos que se produce un error si se busca una prueba con id=2
        prueba3 = self.prueba.filter(id=3).count()
        self.assertEqual(prueba3, 1) # Comprobamos que solo existe una prueba con id=3

        with self.assertRaises(IntegrityError):
            # Comprobamos que se produce un error si se intenta insertar una prueba con id ya existente.
            self.prueba.create(id=1, NomPrueba="Prueba4", NumPreguntas=25, PruVisible=True)

    def test_Progreso(self):
        nFilas = len(self.progreso.all())
        self.assertEqual(nFilas, 3) # Comprobamos que la tabla de progreso tiene inicialmente 3 filas.
        
        self.progreso2.delete()  # Borramos la fila correspondiente al progreso de id=2

        nFilas = len(self.progreso.all())
        self.assertEqual(nFilas, 2) # Comprobamos que, al borrar una fila, la tabla de progreso ahora tiene 2 filas.

        progreso1 = self.progreso.filter(id=1).count()
        self.assertEqual(progreso1, 1) # Comprobamos que solo existe un progreso con id=1
        with self.assertRaises(self.progreso.model.DoesNotExist):
            self.progreso.get(id=2) # Comprobamos que se produce un error si se busca un progreso con id=2
        progreso3 = self.progreso.filter(id=3).count()
        self.assertEqual(progreso3, 1) # Comprobamos que solo existe un progreso con id=3

        with self.assertRaises(IntegrityError):
            # Comprobamos que se produce un error si se intenta insertar un progreso con id ya existente.
            self.progreso.create(id=1, Nota=8.5, PregAcertadas=16, PregFalladas=2, PregBlanco=0, Tiempo=722, IdPrueba_id=1)

    def test_Formado_por(self):
        nFilas = len(self.formado_por.all())
        self.assertEqual(nFilas, 3) # Comprobamos que la tabla de formado_por tiene inicialmente 3 filas.
        
        self.formado_por2.delete()  # Borramos la fila correspondiente al campo de id=2

        nFilas = len(self.formado_por.all())
        self.assertEqual(nFilas, 2) # Comprobamos que, al borrar una fila, la tabla de formado_por ahora tiene 2 filas.

        formado_por1 = self.formado_por.filter(id=1).count()
        self.assertEqual(formado_por1, 1) # Comprobamos que solo existe un campo con id=1
        with self.assertRaises(self.formado_por.model.DoesNotExist):
            self.formado_por.get(id=2) # Comprobamos que se produce un error si se busca un campo con id=2
        formado_por3 = self.formado_por.filter(id=3).count()
        self.assertEqual(formado_por3, 1) # Comprobamos que solo existe un campo con id=3

        with self.assertRaises(IntegrityError):
            # Comprobamos que se produce un error si se intenta insertar un campo con id ya existente.
            self.formado_por.create(id=1, IdTemario_id=1, IdPrueba_id=3)