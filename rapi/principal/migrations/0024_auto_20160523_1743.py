# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 17:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0023_auto_20160523_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atencion',
            name='NroEdiciones',
        ),
        migrations.DeleteModel(
            name='Edicion',
        ),
    ]