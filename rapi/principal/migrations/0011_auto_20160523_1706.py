# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 17:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0010_auto_20160523_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edicion',
            name='TiempoE',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 17, 6, 55, 54000)),
        ),
    ]