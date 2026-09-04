from django.db import models
from accounts.models import Student


class ChatSession(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='ai_chat_sessions'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"AI Chat - "
            f"{self.student.student_id}"
        )


class ChatMessage(models.Model):

    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ASSISTANT', 'Assistant'),
    ]

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.role} - "
            f"{self.session.student.student_id}"
        )