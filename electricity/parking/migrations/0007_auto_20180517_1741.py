# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-17 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0006_cameraparkingspot_rotation_angle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cameraparkingspot',
            name='bottom_left_x',
        ),
        migrations.RemoveField(
            model_name='cameraparkingspot',
            name='bottom_right_y',
        ),
        migrations.RemoveField(
            model_name='cameraparkingspot',
            name='upper_right_x',
        ),
        migrations.RemoveField(
            model_name='cameraparkingspot',
            name='upper_right_y',
        ),
        migrations.AddField(
            model_name='cameraparkingspot',
            name='center_x',
            field=models.IntegerField(default=1, verbose_name='Center x'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cameraparkingspot',
            name='center_y',
            field=models.IntegerField(default=1, verbose_name='Center y'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cameraparkingspot',
            name='height',
            field=models.IntegerField(default=1, verbose_name='Height'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cameraparkingspot',
            name='width',
            field=models.IntegerField(default=1, verbose_name='Width'),
            preserve_default=False,
        ),
    ]