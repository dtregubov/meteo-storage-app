"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import ForecastView, InfoView, MeasurementView, MeteorologicalStationView, SensorView, receive_meteo_data

urlpatterns = [
    # admin route, opens by default for server
    path('admin/', admin.site.urls),

    # swagger routes
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),  # if its necessary to download api doc schema
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs',),

    # app routes
    path('info/', InfoView.as_view(), name='info'),
    path('measurements/', MeasurementView.as_view(), name='measurements'),
    path('sensors/', SensorView.as_view(), name='sensors'),
    path('meteo-stations/', MeteorologicalStationView.as_view(), name='meteo-stations'),
    path('forecasts/', ForecastView.as_view(), name='forecasts'),

    # recieve data
    path('receive-meteo-data/', receive_meteo_data, name='receive_meteo_data'),
]
