from django.contrib import admin
from .models import TransportRoute, TransportStop


class TransportStopInline(admin.TabularInline):

    model = TransportStop

    extra = 1

    ordering = ['stop_order']


@admin.register(TransportRoute)
class TransportRouteAdmin(admin.ModelAdmin):

    list_display = (
        'route_number',
        'name',
        'start_point',
        'end_point',
        'bus_number',
        'departure_time',
        'arrival_time',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'route_number',
        'name',
        'start_point',
        'end_point',
        'bus_number',
    )

    inlines = [
        TransportStopInline
    ]


@admin.register(TransportStop)
class TransportStopAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'area',
        'route',
        'latitude',
        'longitude',
        'pickup_time',
        'is_active',
    )

    list_filter = (
        'is_active',
        'route',
    )

    search_fields = (
        'name',
        'area',
        'route__route_number',
        'route__name',
    )