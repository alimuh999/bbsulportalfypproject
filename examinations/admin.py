from django.contrib import admin
from django.utils import timezone

from .models import ExamForm, ExamFormSubject


@admin.action(description='Approve selected exam forms')
def approve_exam_forms(modeladmin, request, queryset):

    updated_count = queryset.update(
        status='APPROVED',
        rejection_reason='',
        approved_at=timezone.now()
    )

    modeladmin.message_user(
        request,
        f'{updated_count} exam form(s) approved successfully.'
    )


@admin.action(description='Reject selected exam forms')
def reject_exam_forms(modeladmin, request, queryset):

    updated_count = queryset.update(
        status='REJECTED',
        approved_at=None,
        rejection_reason='Rejected by administration.'
    )

    modeladmin.message_user(
        request,
        f'{updated_count} exam form(s) rejected.'
    )


@admin.register(ExamForm)
class ExamFormAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'exam_type',
        'academic_session',
        'semester',
        'status',
        'submitted_at',
        'approved_at',
    )

    list_filter = (
        'exam_type',
        'semester',
        'status',
    )

    search_fields = (
        'student__student_id',
        'student__user__first_name',
        'student__user__last_name',
    )

    readonly_fields = (
        'submitted_at',
        'approved_at',
        'created_at',
    )

    actions = [
        approve_exam_forms,
        reject_exam_forms,
    ]

    fieldsets = (
        (
            'Student Information',
            {
                'fields': (
                    'student',
                    'exam_type',
                    'academic_session',
                    'semester',
                )
            }
        ),
        (
            'Form Status',
            {
                'fields': (
                    'status',
                    'rejection_reason',
                    'submitted_at',
                    'approved_at',
                    'created_at',
                )
            }
        ),
    )


@admin.register(ExamFormSubject)
class ExamFormSubjectAdmin(admin.ModelAdmin):

    list_display = (
        'exam_form',
        'result',
    )

    search_fields = (
        'exam_form__student__student_id',
        'result__subject_code',
        'result__subject_name',
    )