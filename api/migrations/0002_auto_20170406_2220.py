# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
