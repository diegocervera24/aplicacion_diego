from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, nombre, password=None):
        user = self.model(
            username=username,
            email = self.normalize_email(email),
            nombre = nombre,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username,email,nombre,password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            nombre = nombre,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(null=False, max_length=100, primary_key=True)
    email = models.EmailField(null=False, max_length=100,unique=True)
    nombre = models.CharField(null=False, max_length=100)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombre']

    objects = UserManager()

    def __str__(self):
        return self.email + ", " + self.nombre
    
    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        db_table = "USUARIO"