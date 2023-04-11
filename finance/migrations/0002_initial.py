# Generated by Django 4.1.5 on 2023-04-10 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obs', models.CharField(blank=True, max_length=6, null=True)),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('data', models.DateField(blank=True)),
                ('valor', models.CharField(blank=True, max_length=10, null=True)),
                ('movimento', models.CharField(blank=True, max_length=10, null=True)),
                ('hora', models.TimeField(blank=True)),
                ('tipo_pgto', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]