# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 22:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('coord_longitude', models.FloatField(default=0.0)),
                ('coord_latitude', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('temperature', models.IntegerField(default=0)),
                ('pressure', models.IntegerField(default=0)),
                ('humidity', models.IntegerField(default=0)),
                ('wind_speed', models.FloatField(default=0.0)),
                ('wind_deg', models.FloatField(default=0.0)),
                ('weather_desciption', models.CharField(max_length=250)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Weather.City')),
            ],
        ),
    ]