from django.db import models
from accounts.models import Student


class LeaveRequest(models.Model):

    LEAVE_TYPE_CHOICES = [
        ('SICK', 'Sick Leave'),
        ('CASUAL', 'Casual Leave'),
        ('EMERGENCY', 'Emergency Leave'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPE_CHOICES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    attachment = models.FileField(
        upload_to='leave_attachments/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    admin_remarks = models.TextField(
        blank=True
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.get_leave_type_display()} - "
            f"{self.start_date}"
        )