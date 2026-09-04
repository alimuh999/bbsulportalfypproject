from django.db import models
from accounts.models import Student
from academics.models import Result
from django.utils import timezone


class ExamForm(models.Model):

    EXAM_TYPE_CHOICES = [
        ('MIDTERM', 'Midterm'),
        ('FINAL', 'Final'),
        ('SUPPLEMENTARY', 'Supplementary'),
        ('IMPROVEMENT', 'Improvement'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='exam_forms'
    )

    exam_type = models.CharField(
        max_length=20,
        choices=EXAM_TYPE_CHOICES
    )

    academic_session = models.CharField(
        max_length=30
    )

    semester = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    rejection_reason = models.TextField(
        blank=True
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
    null=True,
    blank=True
    )

    def approve(self):
        self.status = 'APPROVED'
        self.rejection_reason = ''
        self.approved_at = timezone.now()
        self.save()

    def reject(self, reason=''):
        self.status = 'REJECTED'
        self.rejection_reason = reason
        self.approved_at = None
        self.save()

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.get_exam_type_display()} - "
            f"Semester {self.semester}"
        )


class ExamFormSubject(models.Model):

    exam_form = models.ForeignKey(
        ExamForm,
        on_delete=models.CASCADE,
        related_name='selected_subjects'
    )

    result = models.ForeignKey(
        Result,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"{self.exam_form.student.student_id} - "
            f"{self.result.subject_code}"
        )