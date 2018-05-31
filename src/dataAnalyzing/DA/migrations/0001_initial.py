# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustDataSchem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('owner', models.CharField(max_length=200)),
                ('pub_date', models.DateField(verbose_name='Date Published')),
                ('db_created', models.BooleanField()),
            ],
        ),
    ]
