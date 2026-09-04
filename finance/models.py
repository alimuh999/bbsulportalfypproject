from django.db import models
from accounts.models import Student


class FeeVoucher(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='fee_vouchers'
    )

    semester = models.PositiveIntegerField()

    voucher_number = models.CharField(
        max_length=50,
        unique=True
    )

    issue_date = models.DateField(
        auto_now_add=True
    )

    due_date = models.DateField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    paid_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def is_paid(self):
        return self.status == 'PAID'

    def __str__(self):
        return (
            f"{self.voucher_number} - "
            f"{self.student.student_id}"
        )