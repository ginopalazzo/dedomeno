# Generated by Django 2.0.1 on 2018-02-13 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0124_auto_20180209_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geocode',
            name='d00',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d01',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d02',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d03',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d04',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d05',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d06',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d07',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d08',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d09',
        ),
        migrations.RemoveField(
            model_name='geocode',
            name='d10',
        ),
        migrations.AlterField(
            model_name='territorialentity',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='father', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='houses.TerritorialEntity'),
        ),
        migrations.DeleteModel(
            name='GeoCode',
        ),
    ]
