import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Forecast, Info, Measurement, MeteorologicalStation, Sensor
from .serializers import (
    ForecastSerializer,
    InfoSerializer,
    MeasurementSerializer,
    MeteorologicalStationSerializer,
    SensorSerializer,
)
from .tasks import store_meteo_data_task


class InfoView(ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer


class MeasurementView(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class SensorView(ListCreateAPIView):
    def get_queryset(self):  # as example of using filtering one query parameter
        sensor_id = self.request.query_params.get('sensor_id')

        if sensor_id is not None:
            return Sensor.objects.filter(sensor_id=sensor_id)
        return Sensor.objects.all()

    serializer_class = SensorSerializer


# User will have an opportunity to create, update, delete meteorological station using Admin
# We can setup API for that if needed just using GenericAPIView and write methods manually.
class MeteorologicalStationView(ListAPIView):
    serializer_class = MeteorologicalStationSerializer
    lookup_field = 'code'

    def get_queryset(self):  # as example of using filtering by several query parameters
        code = self.request.query_params.get('code')
        city = self.request.query_params.get('city')

        meteorological_station_qs = MeteorologicalStation.objects.all()
        if code is not None:
            meteorological_station_qs = meteorological_station_qs.filter(code=code)
        if city is not None:
            meteorological_station_qs = meteorological_station_qs.filter(city=city)

        return meteorological_station_qs


# CreateAPIView was added just for testing purposes
class ForecastView(RetrieveAPIView, CreateAPIView):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer


# No documentation, but can be added by drf_yasg swagger_auto_schema
@api_view(['POST'])
def receive_meteo_data(request: Request) -> Response:
    data = request.data
    store_meteo_data_task.delay(data)  # to process asynchronously
    return Response({'message': 'Data received.'}, status=status.HTTP_202_ACCEPTED)


def send_forecast(forecast: Forecast) -> Response:
    print(forecast)
    serializer = ForecastSerializer(
        data={
            'forecast_date': forecast.forecast_date,
            'city': forecast.city,
            'temperature': forecast.temperature,
            'humidity': forecast.humidity,
            'wind': forecast.wind,
        }
    )
    serializer.is_valid(raise_exception=True)

    data_to_send = {
        'forecast_date': serializer.validated_data['forecast_date'].isoformat(),
        'city': serializer.validated_data['city'],
        'temperature': serializer.validated_data['temperature'],
        'humidity': serializer.validated_data['humidity'],
        'wind': serializer.validated_data['wind']
    }

    try:
        # Send the data to some remote server as example - used my server to test (it created the same forecast)
        response = requests.post('http://0.0.0.0:8001/forecasts/', json=data_to_send, timeout=5)
        print(*response)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return Response({'message': 'Forecast sent to remote server successfully'}, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        # Handle errors if they come during the HTTP request
        return Response(
            {'message': 'Forecast failed to send to remote server', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
