# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0086_remove_property_equipment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='people_now_living_gender',
        ),
        migrations.AddField(
            model_name='room',
            name='people_now_living_female',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='room',
            name='people_now_living_male',
            field=models.NullBooleanField(),
        ),
    ]
