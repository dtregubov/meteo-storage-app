"""
Tests for the Django admin modifications.
"""
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from api import models


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create superuser and log in. Create Meteo station."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)

        self.meteorogical_station = models.MeteorologicalStation.objects.create(
            code='test_code',
            city='Funchal',
            latitude=1.234,
            longitude=1.432,
            date_of_installation=datetime(2024, 7, 16),
        )

    # Wrote example of Admin test for a page, meteo station in this case, should be extended for all pages
    def test_meteo_station_list(self):
        """Test that meteo stations are listed on page."""
        url = reverse('admin:api_meteorologicalstation_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.meteorogical_station.code)
        self.assertContains(res, self.meteorogical_station.city)
        self.assertContains(res, self.meteorogical_station.latitude)
        self.assertContains(res, self.meteorogical_station.longitude)

    def test_edit_meteo_station_page(self):
        """Test the edit meteo station page works."""
        url = reverse('admin:api_meteorologicalstation_change', args=[self.meteorogical_station.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_meteo_station_page(self):
        """Test the create meteo station page works."""
        url = reverse('admin:api_meteorologicalstation_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
