# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-06-02 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0026_auto_20160602_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atencion',
            name='NroEdiciones',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='principal.Edicion'),
        ),
    ]
