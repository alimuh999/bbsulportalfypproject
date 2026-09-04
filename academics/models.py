from django.db import models
from accounts.models import Student


class Result(models.Model):

    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='results'
    )

    semester = models.PositiveIntegerField(
        choices=SEMESTER_CHOICES
    )

    subject_code = models.CharField(
        max_length=30
    )

    subject_name = models.CharField(
        max_length=150
    )

    credit_hours = models.PositiveIntegerField(
        default=3
    )

    obtained_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    total_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def percentage(self):

        if self.total_marks == 0:
            return 0

        return round(
            (float(self.obtained_marks) /
             float(self.total_marks)) * 100,
            2
        )

    def grade(self):

        percentage = self.percentage()

        if percentage >= 80:
            return 'A+'

        elif percentage >= 70:
            return 'A'

        elif percentage >= 60:
            return 'B'

        elif percentage >= 50:
            return 'C'

        elif percentage >= 40:
            return 'D'

        else:
            return 'F'

    def __str__(self):

        return f"{self.student.student_id} - {self.subject_name}"


# ==========================================
# MARKSHEET
# ==========================================

class Marksheet(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='marksheets'
    )

    semester = models.PositiveIntegerField(
        choices=Result.SEMESTER_CHOICES
    )

    issue_date = models.DateField(
        auto_now_add=True
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.student.student_id} - "
            f"Semester {self.semester}"
        )