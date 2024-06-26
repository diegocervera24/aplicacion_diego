# Generated by Django 5.0.3 on 2024-05-10 17:22

import django.core.validators
import django.db.models.deletion
import oposicion.models
from django.conf import settings
from django.db import migrations, models

def cargar_datos(apps, schema_editor):
    Oposicion = apps.get_model('oposicion', 'Oposicion')
    Oposicion.objects.create(NomOposicion='Acceso a la Carrera Judicial y Fiscal')
    Oposicion.objects.create(NomOposicion='Letrados de la Administración de Justicia')
    Oposicion.objects.create(NomOposicion='Gestión Procesal y Administrativa')
    Oposicion.objects.create(NomOposicion='Tramitación Procesal y Administrativa de la Administración de Justicia')
    Oposicion.objects.create(NomOposicion='Auxilio Judicial')
    Oposicion.objects.create(NomOposicion='Tramitación Procesal')
    Oposicion.objects.create(NomOposicion='Ayudantes de Instituciones Penitenciarias')
    Oposicion.objects.create(NomOposicion='Administrativos del Estado, especialidad Tráfico')
    Oposicion.objects.create(NomOposicion='Policía Nacional Escala Ejecutiva')
    Oposicion.objects.create(NomOposicion='Policía Nacional Escala Básica')
    Oposicion.objects.create(NomOposicion='Guardia Civil')
    Oposicion.objects.create(NomOposicion='Policía Local')
    Oposicion.objects.create(NomOposicion='Agentes de la Hacienda Pública')
    Oposicion.objects.create(NomOposicion='Auxiliar de Administración e Información')
    Oposicion.objects.create(NomOposicion='Gestión de la Administración Civil del Estado')
    Oposicion.objects.create(NomOposicion='Administrativos del Estado')
    Oposicion.objects.create(NomOposicion='Auxiliares Administrativos del Estado')
    Oposicion.objects.create(NomOposicion='Técnicos Auxiliares de Informática de la Administración del Estado')
    Oposicion.objects.create(NomOposicion='Ayudantes de Investigación de los Organismos Públicos de Investigación')
    Oposicion.objects.create(NomOposicion='Gestión de la Administración de la Seguridad Social')
    Oposicion.objects.create(NomOposicion='Administrativos de la Seguridad Social')
    Oposicion.objects.create(NomOposicion='Auxiliares Administrativos')
    Oposicion.objects.create(NomOposicion='Ujieres de las Cortes Generales')
    Oposicion.objects.create(NomOposicion='Administrativos')
    Oposicion.objects.create(NomOposicion='Auxiliares Administrativos')
    Oposicion.objects.create(NomOposicion='Bomberos forestales')
    Oposicion.objects.create(NomOposicion='Prueba Acceso a la Abogacía')
    Oposicion.objects.create(NomOposicion='Corporaciones locales')
    Oposicion.objects.create(NomOposicion='Auxiliar Administrativo Ayuntamiento')
    Oposicion.objects.create(NomOposicion='Agentes Medioambientales Organismos Autónomos')
    Oposicion.objects.create(NomOposicion='Celador/a')
    Oposicion.objects.create(NomOposicion='Celador Conductor')
    Oposicion.objects.create(NomOposicion='TCAE')
    Oposicion.objects.create(NomOposicion='Auxiliar Administrativo de Servicios Sanitarios')
    Oposicion.objects.create(NomOposicion='Médico de Urgencias Hospitalarias')
    Oposicion.objects.create(NomOposicion='Médico de Familia')
    Oposicion.objects.create(NomOposicion='Enfermería')
    Oposicion.objects.create(NomOposicion='Correos')
    Oposicion.objects.create(NomOposicion='Tropa y Marinería')

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Oposicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NomOposicion', models.CharField(max_length=100)),
                ('OpoVisible', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'OPOSICION',
            },
        ),
        
        migrations.RunPython(cargar_datos),
    
        migrations.CreateModel(
            name='Prueba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NomPrueba', models.CharField(max_length=50)),
                ('NumPreguntas', models.DecimalField(decimal_places=0, max_digits=2)),
                ('PruVisible', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'PRUEBA',
            },
        ),
        migrations.CreateModel(
            name='Progreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nota', models.DecimalField(decimal_places=2, max_digits=4)),
                ('PregAcertadas', models.DecimalField(decimal_places=0, max_digits=3)),
                ('PregFalladas', models.DecimalField(decimal_places=0, max_digits=3)),
                ('PregBlanco', models.DecimalField(decimal_places=0, max_digits=3)),
                ('Tiempo', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('IdPrueba', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oposicion.prueba')),
            ],
            options={
                'db_table': 'PROGRESO',
            },
        ),
        migrations.CreateModel(
            name='Temario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NomTemario', models.CharField(max_length=50)),
                ('NumPaginas', models.DecimalField(decimal_places=0, max_digits=4)),
                ('TemVisible', models.BooleanField(default=True)),
                ('Archivo', models.FileField(upload_to=oposicion.models.path_usuario_temario)),
                ('IdOposicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oposicion.oposicion')),
                ('NomUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'TEMARIO',
            },
        ),
        migrations.CreateModel(
            name='Formado_por',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IdPrueba', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oposicion.prueba')),
                ('IdTemario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oposicion.temario')),
            ],
            options={
                'db_table': 'FORMADO_POR',
            },
        ),
        migrations.AddConstraint(
            model_name='formado_por',
            constraint=models.UniqueConstraint(fields=('IdTemario', 'IdPrueba'), name='pk_IdTemario_IdPrueba'),
        ),
    ]
