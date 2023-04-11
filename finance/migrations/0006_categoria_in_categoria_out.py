# Generated by Django 4.1.5 on 2023-04-10 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_rename_categoria_finance_categoria_in_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='categoria_in',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='categoria_out',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]