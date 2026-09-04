from django.db import models
from django.utils import timezone

from accounts.models import Student


class DegreeClearance(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='degree_clearance'
    )

    application_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    remarks = models.TextField(
        blank=True
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.application_number:
            year = timezone.now().year

            last_application = (
                DegreeClearance.objects
                .filter(application_number__startswith=f'DC-{year}-')
                .order_by('-id')
                .first()
            )

            if last_application:
                try:
                    last_number = int(
                        last_application.application_number.split('-')[-1]
                    )
                except (ValueError, IndexError):
                    last_number = 0
            else:
                last_number = 0

            self.application_number = (
                f'DC-{year}-{last_number + 1:05d}'
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.application_number} - "
            f"{self.student.student_id}"
        )