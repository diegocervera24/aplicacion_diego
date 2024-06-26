from django.db import models
from usuarios.models import User
from django.core.validators import MinValueValidator

def path_usuario_temario(instance, filename):
    # instance.user es el usuario que sube el archivo
    return f'{instance.NomUsuario.username}/{filename}'

class Oposicion(models.Model):
    NomOposicion = models.CharField(null=False, max_length=100)
    OpoVisible = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.NomOposicion

    class Meta:
        db_table = "OPOSICION"


class Temario(models.Model):
    NomTemario = models.CharField(null=False, max_length=50)
    NumPaginas = models.DecimalField(null=False, max_digits=4, decimal_places=0)
    TemVisible = models.BooleanField(null=False, default=True)
    Archivo = models.FileField(upload_to=path_usuario_temario, null=False)
    NomUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    IdOposicion = models.ForeignKey(Oposicion, on_delete=models.CASCADE)

    def __str__(self):
        return self.NomTemario
    
    class Meta:
        db_table = "TEMARIO"
    
class Prueba(models.Model):
    NomPrueba = models.CharField(null=False, max_length=50)
    NumPreguntas = models.DecimalField(null=False, max_digits=2, decimal_places=0)
    PruVisible = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.NomPrueba
    
    class Meta:
        db_table = "PRUEBA"
    
class Progreso(models.Model):
    Nota = models.DecimalField(null=False, max_digits=4, decimal_places=2)
    PregAcertadas = models.DecimalField(null=False, max_digits=3, decimal_places=0)
    PregFalladas = models.DecimalField(null=False, max_digits=3, decimal_places=0)
    PregBlanco = models.DecimalField(null=False, max_digits=3, decimal_places=0)
    Tiempo = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    IdPrueba = models.ForeignKey(Prueba, on_delete=models.CASCADE)

    class Meta:
        db_table = "PROGRESO" 

class Formado_por(models.Model):
    IdTemario = models.ForeignKey(Temario, on_delete=models.CASCADE)
    IdPrueba = models.ForeignKey(Prueba, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['IdTemario', 'IdPrueba'], name='pk_IdTemario_IdPrueba'
            )
        ]

        db_table = "FORMADO_POR"