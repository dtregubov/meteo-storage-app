from django.contrib import admin
from django_celery_beat.admin import PeriodicTaskAdmin
from django_celery_beat.models import PeriodicTask

from .models import Forecast, Info, Measurement, MeteorologicalStation, Sensor
from .utils import action_on_entity
from .views import send_forecast


class CustomFilteringOptionsPeriodicTaskAdmin(PeriodicTaskAdmin):
    list_filter = ['enabled', 'one_off', 'start_time', 'last_run_at']


admin_site = admin.AdminSite(name='admin')
admin_site.register(PeriodicTask, CustomFilteringOptionsPeriodicTaskAdmin)  # Open an ability see tasks in Admin


class InfoInline(admin.TabularInline):  # just as an example - usually useful to have inlines
    model = Info
    extra = 1


@admin.register(MeteorologicalStation)
class MeteorologicalStationAdmin(admin.ModelAdmin):
    list_display = ('code', 'city', 'latitude', 'longitude', 'date_of_installation')
    search_fields = ('code', 'city')
    list_filter = ('city', 'date_of_installation')


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'station', 'property_type')
    search_fields = ('sensor_id', 'station__code', 'station__city')
    list_filter = ('property_type', 'station__city')


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'sensor', 'date', 'city')
    search_fields = ('identifier', 'sensor__sensor_id', 'city')
    list_filter = ('sensor__station__city', 'date')
    inlines = [InfoInline]


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('measurement', 'category', 'measurement_value', 'unit')
    search_fields = ('measurement__identifier', 'category')
    list_filter = ('category', 'unit')


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('forecast_date', 'city', 'temperature', 'humidity', 'wind')
    search_fields = ('city',)
    list_filter = ('forecast_date', 'city')
    actions = {
        'send_forecast_for_city',
    }

    @action_on_entity(
        success_message='Forecast was sent!',
        error_message='Failed to send forecast {entity}: {error}',
    )
    def send_forecast_for_city(self, request, forecast: Forecast):
        send_forecast(forecast)

    send_forecast_for_city.short_description = 'Send chosen forecast to the city'
