from django.contrib import admin

from .models import (
    ChatSession,
    ChatMessage
)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'student__student_id',
        'student__user__first_name',
        'student__user__last_name',
    )

    ordering = (
        '-updated_at',
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'session',
        'role',
        'created_at',
    )

    list_filter = (
        'role',
        'created_at',
    )

    search_fields = (
        'message',
        'session__student__student_id',
    )

    ordering = (
        '-created_at',
    )