# Generated by Django 5.1.1 on 2024-10-11 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carbono', '0002_carros_emissao'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Carros',
            new_name='Carro',
        ),
    ]