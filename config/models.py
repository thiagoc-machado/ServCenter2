from django.db import models

class Config(models.Model):
    nome_empresa = models.CharField(max_length=100, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    atividade = models.CharField(max_length=100, blank=True, null=True)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    logo1 = models.ImageField(upload_to='logos', blank=True, null=True)
    logo2 = models.ImageField(upload_to='logos', blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.nome_empresa    