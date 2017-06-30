from django.db import models
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    coord_longitude = models.FloatField(default=0.0)
    coord_latitude = models.FloatField(default=0.0)


class Info(models.Model):
    city = models.ForeignKey(City)
    date = models.DateTimeField(default=timezone.now)
    temperature = models.IntegerField(default=0)
    pressure = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    wind_speed = models.FloatField(default=0.0)
    weather_description = models.CharField(max_length=250)

