from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
'''
from django.contrib.auth import get_user_model
User = get_user_model()
'''
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True)
    nome = models.CharField('nome', max_length=30, blank=False)
    dre = models.CharField('dre', max_length=9, blank=True)
    is_staff = models.BooleanField('Eh da equipe?',blank=True,default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_nome(self):
        
        return self.nome



class Palestra(models.Model):
    
    tema = models.CharField(max_length=100, unique=True)
    palestrante = models.CharField(max_length=100)
    descricao_palestra = models.CharField(max_length=1000)
    descricao_palestrante = models.CharField(max_length=1000)
    foto_palestrante = models.ImageField(blank=True,null=True,upload_to="fotos")
    sala = models.CharField(max_length=20)
    inicio = models.TimeField()
    termino = models.TimeField()
    dia = models.CharField(max_length=10)
    

    favorito = models.ManyToManyField(User, related_name="favorito", blank=True) 
    foi_na_palestra = models.ManyToManyField(User, related_name="foi_na_palestra", blank=True) 

    
    def __str__(self):
        return self.tema + " - " + self.palestrante 



class Parceiro(models.Model):
    
    logo = models.ImageField(blank=True,null=True,upload_to="fotos")


class Form(models.Model):


    owner = models.ForeignKey('api.User', on_delete=models.CASCADE)

    pa_id = models.ForeignKey(Palestra, on_delete=models.CASCADE)

    Pergunta1 = models.CharField(max_length=100)
    Pergunta2 = models.CharField(max_length=100)
    Pergunta3 = models.CharField(max_length=100)
    Pergunta4 = models.CharField(max_length=100)
    Pergunta5 = models.CharField(max_length=100)

class Cores(models.Model):
    primaria = models.CharField(max_length=7)
    secundaria = models.CharField(max_length=7)
    terciaria = models.CharField(max_length=7)
    quaternaria = models.CharField(max_length=7)

 
