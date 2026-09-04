import math

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import TransportRoute, TransportStop


def calculate_distance(lat1, lon1, lat2, lon2):

    radius = 6371

    lat1 = math.radians(float(lat1))
    lon1 = math.radians(float(lon1))
    lat2 = math.radians(float(lat2))
    lon2 = math.radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return radius * c


@login_required
def transport_routes(request):

    student = request.user.student_profile

    routes = TransportRoute.objects.filter(
        is_active=True
    ).prefetch_related('stops')

    nearest_stops = []

    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    if latitude and longitude:

        try:

            user_latitude = float(latitude)
            user_longitude = float(longitude)

            for stop in TransportStop.objects.filter(
                is_active=True,
                route__is_active=True
            ).select_related('route'):

                distance = calculate_distance(
                    user_latitude,
                    user_longitude,
                    stop.latitude,
                    stop.longitude
                )

                if distance <= 15:

                    nearest_stops.append({
                        'stop': stop,
                        'distance': round(distance, 2),
                    })

            nearest_stops.sort(
                key=lambda x: x['distance']
            )

            nearest_stops = nearest_stops[:10]

        except (ValueError, TypeError):

            nearest_stops = []

    return render(
        request,
        'transport/routes.html',
        {
            'student': student,
            'routes': routes,
            'nearest_stops': nearest_stops,
            'latitude': latitude,
            'longitude': longitude,
        }
    )