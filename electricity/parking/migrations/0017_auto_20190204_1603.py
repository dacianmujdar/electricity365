# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-04 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0016_auto_20190204_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkinglane',
            name='right_y',
            field=models.IntegerField(verbose_name='Median line y right'),
        ),
    ]
