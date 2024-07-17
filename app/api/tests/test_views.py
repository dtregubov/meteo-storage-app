from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import MeteorologicalStation


@pytest.fixture(name='test_api_client')
def api_client():
    return APIClient()


@pytest.fixture(name='create_meteo_station')
def create_station():
    def make_station(**kwargs):
        return MeteorologicalStation.objects.create(**kwargs)
    return make_station


@pytest.mark.django_db
def test_get_stations_no_filter(test_api_client, create_meteo_station):
    # Create test data
    create_meteo_station(
        code='test_code1', city='Funchal', latitude=1.234, longitude=1.432, date_of_installation=datetime(2024, 7, 16)
    )
    create_meteo_station(
        code='test_code2', city='London', latitude=2.234, longitude=2.432, date_of_installation=datetime(2024, 7, 17)
    )

    # Make a request to the view
    url = reverse('meteo-stations')
    response = test_api_client.get(url)

    # Check the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_stations_filter_by_code(test_api_client, create_meteo_station):
    # Create test data
    code1 = 'test_code1'
    code2 = 'test_code2'
    create_meteo_station(
        code=code1, city='Funchal', latitude=1.234, longitude=1.432, date_of_installation=datetime(2024, 7, 16)
    )
    create_meteo_station(
        code=code2, city='London', latitude=2.234, longitude=2.432, date_of_installation=datetime(2024, 7, 17)
    )

    # Make a request to the view with a code filter
    url = reverse('meteo-stations')
    response = test_api_client.get(url, {'code': code1})

    # Check the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['code'] == code1


@pytest.mark.django_db
def test_get_stations_filter_by_city(test_api_client, create_meteo_station):
    # Create test data
    city1 = 'Funchal'
    city2 = 'London'
    create_meteo_station(
        code='test_code1', city=city1, latitude=1.234, longitude=1.432, date_of_installation=datetime(2024, 7, 16)
    )
    create_meteo_station(
        code='test_code2', city=city2, latitude=2.234, longitude=2.432, date_of_installation=datetime(2024, 7, 17)
    )

    # Make a request to the view with a city filter
    url = reverse('meteo-stations')
    response = test_api_client.get(url, {'city': city1})

    # Check the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['city'] == city1


@pytest.mark.django_db
def test_get_stations_filter_by_code_and_city(test_api_client, create_meteo_station):
    # Create test data
    code1 = 'test_code1'
    code2 = 'test_code2'
    code3 = 'test_code3'
    city1 = 'Funchal'
    city2 = 'London'
    city3 = 'Hong-Cong'
    create_meteo_station(
        code=code1, city=city1, latitude=1.234, longitude=1.432, date_of_installation=datetime(2024, 7, 16)
    )
    create_meteo_station(
        code=code2, city=city2, latitude=2.234, longitude=2.432, date_of_installation=datetime(2024, 7, 17)
    )
    create_meteo_station(
        code=code3, city=city3, latitude=3.234, longitude=3.432, date_of_installation=datetime(2024, 7, 18)
    )

    # Make a request to the view with a code and city filter
    url = reverse('meteo-stations')
    response = test_api_client.get(url, {'code': code3, 'city': city3})

    # Check the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['code'] == code3
    assert response.data[0]['city'] == city3
