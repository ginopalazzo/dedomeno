# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0051_auto_20161226_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcehouse',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='houses.Source'),
        ),
    ]
