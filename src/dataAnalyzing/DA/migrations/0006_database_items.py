# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DA', '0005_database_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='items',
            field=models.IntegerField(default=0),
        ),
    ]
