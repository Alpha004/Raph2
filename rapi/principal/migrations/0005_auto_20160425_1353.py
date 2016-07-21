# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 18:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0004_remove_atencion_fechaa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atencion',
            name='DescripcionA',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='atencion',
            name='Estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='atencion',
            name='ID_P',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='principal.Personal'),
        ),
    ]