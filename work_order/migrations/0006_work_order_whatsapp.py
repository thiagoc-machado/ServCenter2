# Generated by Django 4.1.5 on 2023-01-24 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0005_rename_obs_work_order_obs_cli'),
    ]

    operations = [
        migrations.AddField(
            model_name='work_order',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
