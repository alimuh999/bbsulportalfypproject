from django.db import models


class TransportRoute(models.Model):

    name = models.CharField(
        max_length=150
    )

    route_number = models.CharField(
        max_length=50,
        unique=True
    )

    start_point = models.CharField(
        max_length=150
    )

    end_point = models.CharField(
        max_length=150
    )

    bus_number = models.CharField(
        max_length=50,
        blank=True
    )

    departure_time = models.TimeField(
        null=True,
        blank=True
    )

    arrival_time = models.TimeField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.route_number} - {self.name}"


class TransportStop(models.Model):

    route = models.ForeignKey(
        TransportRoute,
        on_delete=models.CASCADE,
        related_name='stops'
    )

    name = models.CharField(
        max_length=150
    )

    area = models.CharField(
        max_length=150,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    stop_order = models.PositiveIntegerField(
        default=1
    )

    pickup_time = models.TimeField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['stop_order']

    def __str__(self):
        return f"{self.route.route_number} - {self.name}"