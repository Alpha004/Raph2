# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-06-22 17:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0029_auto_20160608_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atencion',
            name='Nombre_U',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
