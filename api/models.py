from __future__ import unicode_literals
from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager

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

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    nome = models.CharField(_('nome'), max_length=30, blank=True)
    dre = models.CharField(_('dre'), max_length=9, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_nome(self):

        return self.nome



class Palestra(models.Model):
    
    nome = models.CharField(max_length=100)
    palestrante = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    sala = models.CharField(max_length=20)
    
    data = models.DateTimeField()

    
    def __str__(self):
        return self.nome + " - " + self.palestrante 


class Form(models.Model):
    
	autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	id_palestra = models.ForeignKey(Palestra, on_delete=models.CASCADE)

	Pergunta1 = models.CharField(max_length=100)
	Pergunta2 = models.CharField(max_length=100)
	Pergunta3 = models.CharField(max_length=100)
	Pergunta4 = models.CharField(max_length=100)
	Pergunta5 = models.CharField(max_length=100)


	data = models.DateTimeField()


	def __str__(self):
		return self.nome + " - " + self.palestrante 
