"""
Tests for models.
"""
from datetime import datetime

from django.test import TestCase

from api import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_meteo_station_all_fields_successful(self):
        """Test creating a meteo station with all fields successful."""
        code = 'test_code'
        city = 'Funchal'
        latitude = 1.234
        longitude = 1.432
        date_of_installation = datetime(2024, 7, 16)

        meteorogical_station = models.MeteorologicalStation.objects.create(
            code=code,
            city=city,
            latitude=latitude,
            longitude=longitude,
            date_of_installation=date_of_installation,
        )

        self.assertEqual(meteorogical_station.code, code)
        self.assertEqual(meteorogical_station.city, city)
        self.assertEqual(meteorogical_station.latitude, latitude)
        self.assertEqual(meteorogical_station.longitude, longitude)
        self.assertEqual(meteorogical_station.date_of_installation, date_of_installation)

    def test_create_meteo_station_required_fields_successful(self):
        """Test creating a meteo station with required fields only successful."""
        code = 'test_code'
        city = 'Funchal'

        meteorogical_station = models.MeteorologicalStation.objects.create(
            code=code,
            city=city,
        )

        self.assertEqual(meteorogical_station.code, code)
        self.assertEqual(meteorogical_station.city, city)
        self.assertIsNone(meteorogical_station.latitude)
        self.assertIsNone(meteorogical_station.longitude)
        self.assertIsNone(meteorogical_station.date_of_installation)
