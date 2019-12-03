from django.db import models

# Create your models here.

class Palestra(models.Model):
    nome = models.CharField(max_length=100)
    palestrante = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    sala = models.CharField(max_length=20)
    
    data = models.DateTimeField()

    
    def __str__(self):
        return self.nome + " - " + self.palestrante 

class Form_Satisfacao(models.Model):
    id_palestra = models.ForeignKey(Palestra, on_delete=models.CASCADE)
    
    nome = models.CharField(max_length=100)
    palestrante = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    sala = models.CharField(max_length=20)
    
    data = models.DateTimeField()

    
    def __str__(self):
        return self.nome + " - " + self.palestrante 
