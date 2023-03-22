from django.db import models


class Documents(models.Model):
    documento = models.CharField(max_length=100, blank=True, null=True)
    texto = models.TextField(blank=True, null=True)
    arquivo = models.FileField(
        upload_to='../media/documents', blank=True, null=True)
    foto = models.ImageField(
        upload_to='../media/documents', blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
