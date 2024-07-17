from rest_framework import serializers

from .models import Forecast, Info, Measurement, MeteorologicalStation, Sensor


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class MeteorologicalStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeteorologicalStation
        fields = '__all__'


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = '__all__'
