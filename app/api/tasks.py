import datetime

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone

from api.models import PROPERTY_CHOICES, Forecast, Info, Measurement, MeteorologicalStation, Sensor
from app.celery import app


def create_forecasts(forecast_date: datetime.date) -> None:
    now = timezone.now()  # Get the current time
    # Calculate the start of yesterday (00:00:00)
    yesterday_start_day = (now - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # Calculate the end of yesterday (23:59:59)
    yesterday_end_day = (now - datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)

    cities = Measurement.objects.values_list('city', flat=True).distinct()

    for city in cities:
        # Get the measurements for yesterday
        measurements = Measurement.objects.filter(date__gte=yesterday_start_day, date__lte=yesterday_end_day, city=city)

        # Let's imagine that we think an average propeties will be the forecast for the date
        # Calculate the average values for all PROPERTY_CHOICES
        avg_temperature = Info.objects.filter(
            measurement__in=measurements, category=PROPERTY_CHOICES.temperature,
        ).aggregate(Avg('measurement_value'))['measurement_value__avg']

        avg_humidity = Info.objects.filter(
            measurement__in=measurements, category=PROPERTY_CHOICES.humidity,
        ).aggregate(Avg('measurement_value'))['measurement_value__avg']

        avg_wind = Info.objects.filter(
            measurement__in=measurements, category=PROPERTY_CHOICES.wind,
        ).aggregate(Avg('measurement_value'))['measurement_value__avg']

        # Create a new Forecast record
        Forecast.objects.create(
            forecast_date=forecast_date,
            city=city,
            temperature=avg_temperature,
            humidity=avg_humidity,
            wind=avg_wind,
        )


# example, in real it's better to add some conditions here to prove the input data
def store_meteo_data(data: dict) -> None:
    meteo_station_code = data['code']
    meteo_station = get_object_or_404(MeteorologicalStation, code=meteo_station_code)

    sensors = [data['sensor'] for data['sensor'] in data]
    for sensor in sensors:
        exists = Sensor.objects.filter(sensor_id=sensor.sensor_id).exists()
        if not exists:
            Sensor.objects.create(
                sensor_id=sensor['sensor_id'],
                station=meteo_station,
                property_type=sensor['property_type'],
            )

        measurements = [sensor['measurement'] for sensor['measurement'] in sensor]
        for measurement in measurements:
            Measurement.objects.create(
                identifier=measurement['identifier'],
                sensor=measurement['sensor'],
                date=measurement['date'],
                city=measurement['city'],
            )

            infos = [measurement['info'] for measurement['info'] in measurement]
            for info in infos:
                Info.objects.create(
                    measurement=info['measurement'],
                    category=info['category'],
                    measurement_value=info['measurement_value'],
                    unit=info['unit'],
                )


# Some logic to create the forecast for specific date
@app.task(ignore_result=True)
def create_forecasts_task(forecast_date: datetime.date) -> None:
    create_forecasts(forecast_date)


# I imagine that the data contains all necessary fields starting from Station till Info.
# In some cases we don't need to create objects, for example for MeteoStation
# as it should be created manually from admin as I get from task
@app.task(ignore_result=True)
def store_meteo_data_task(data: dict) -> None:
    store_meteo_data(data)
