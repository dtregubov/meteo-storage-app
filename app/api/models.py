from django.db import models
from model_utils import Choices

PROPERTY_CHOICES = Choices(
    ('temperature', 'Temperature'),
    ('humidity', 'Humidity'),
    ('wind', 'Wind'),
)


class MeteorologicalStation(models.Model):
    code = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=50)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date_of_installation = models.DateField(null=True, blank=True)


class Sensor(models.Model):
    sensor_id = models.CharField(max_length=10, unique=True)
    station = models.ForeignKey(MeteorologicalStation, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=20, choices=PROPERTY_CHOICES)  # example to use PROPERTY_CHOICES.wind


class Measurement(models.Model):
    identifier = models.CharField(max_length=50, unique=True, help_text='Unique uuid for each measurement')
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    city = models.CharField(max_length=50)


class Info(models.Model):
    measurement = models.ForeignKey(Measurement, related_name='info', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=PROPERTY_CHOICES)
    measurement_value = models.FloatField()
    unit = models.CharField(max_length=20)


class Forecast(models.Model):
    forecast_date = models.DateField()
    city = models.CharField(max_length=50)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    wind = models.FloatField(null=True, blank=True)
