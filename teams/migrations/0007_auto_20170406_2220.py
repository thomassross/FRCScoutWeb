# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20170212_0429'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='notes',
            field=models.CharField(blank=True, default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='team',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
