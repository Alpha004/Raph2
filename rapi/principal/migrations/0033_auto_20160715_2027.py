# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-07-15 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0032_paciente_dni_p'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='Dni_P',
            field=models.IntegerField(default=0),
        ),
    ]