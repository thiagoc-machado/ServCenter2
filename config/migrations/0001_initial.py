# Generated by Django 4.1.5 on 2023-03-22 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_empresa', models.CharField(blank=True, max_length=100, null=True)),
                ('nome_fantasia', models.CharField(blank=True, max_length=100, null=True)),
                ('responsavel', models.CharField(blank=True, max_length=100, null=True)),
                ('atividade', models.CharField(blank=True, max_length=100, null=True)),
                ('cnpj', models.CharField(blank=True, max_length=20, null=True)),
                ('endereco', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.CharField(blank=True, max_length=10, null=True)),
                ('bairro', models.CharField(blank=True, max_length=50, null=True)),
                ('cidade', models.CharField(blank=True, max_length=50, null=True)),
                ('estado', models.CharField(blank=True, max_length=2, null=True)),
                ('cep', models.CharField(blank=True, max_length=10, null=True)),
                ('logo1', models.ImageField(blank=True, null=True, upload_to='../media/logos')),
                ('logo2', models.ImageField(blank=True, null=True, upload_to='../media/logos')),
                ('obs', models.TextField(blank=True, null=True)),
                ('data', models.DateField(blank=True, null=True)),
            ],
        ),
    ]