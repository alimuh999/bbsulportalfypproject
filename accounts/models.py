from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    FEE_STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    student_id = models.CharField(
        max_length=30,
        unique=True
    )

    registration_no = models.CharField(
        max_length=50,
        unique=True
    )

    father_name = models.CharField(
        max_length=100
    )

    department = models.CharField(
        max_length=100
    )

    program = models.CharField(
        max_length=100
    )

    semester = models.PositiveIntegerField(
        default=1
    )

    section = models.CharField(
        max_length=20,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='students/',
        blank=True,
        null=True
    )

    fee_status = models.CharField(
        max_length=10,
        choices=FEE_STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def current_fee_status(self):
        """
        Latest fee voucher ka status return karta hai.
        Agar voucher nahi hai to Student ka old fee_status use hoga.
        """

        latest_voucher = self.fee_vouchers.order_by(
            '-issue_date',
            '-id'
        ).first()

        if latest_voucher:
            return latest_voucher.status

        return self.fee_status

    def __str__(self):
        return (
            f"{self.student_id} - "
            f"{self.user.get_full_name()}"
        )