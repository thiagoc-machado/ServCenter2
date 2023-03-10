# Generated by Django 4.1.5 on 2023-01-14 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_client_data_cadastro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='celular',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='cpf',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='data_nasc',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='foto',
            field=models.ImageField(null=True, upload_to='foto_cliente'),
        ),
        migrations.AlterField(
            model_name='client',
            name='rg',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='telefone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='whatsapp',
            field=models.CharField(max_length=14, null=True),
        ),
    ]
