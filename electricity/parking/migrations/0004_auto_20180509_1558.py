# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-09 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0003_auto_20180429_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camerainput',
            name='url',
            field=models.URLField(help_text='The audio stream url', max_length=400),
        ),
    ]
