from django.contrib import admin
from django.utils import timezone

from .models import DegreeClearance


@admin.register(DegreeClearance)
class DegreeClearanceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'application_number',
        'student',
        'status',
        'submitted_at',
        'reviewed_at',
        'approved_at',
    )

    list_filter = (
        'status',
        'created_at',
        'submitted_at',
    )

    search_fields = (
        'application_number',
        'student__student_id',
        'student__registration_no',
        'student__user__first_name',
        'student__user__last_name',
    )

    readonly_fields = (
        'application_number',
        'submitted_at',
        'reviewed_at',
        'approved_at',
        'created_at',
        'updated_at',
    )

    ordering = (
        '-created_at',
    )

    fieldsets = (
        (
            'Student Information',
            {
                'fields': (
                    'student',
                    'application_number',
                )
            }
        ),

        (
            'Clearance Review',
            {
                'fields': (
                    'status',
                    'remarks',
                )
            }
        ),

        (
            'Application Information',
            {
                'fields': (
                    'submitted_at',
                    'reviewed_at',
                    'approved_at',
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    actions = (
        'approve_clearance',
        'reject_clearance',
        'mark_under_review',
    )

    @admin.action(description='Approve selected clearance requests')
    def approve_clearance(self, request, queryset):

        updated = queryset.update(
            status='APPROVED',
            reviewed_at=timezone.now(),
            approved_at=timezone.now(),
        )

        self.message_user(
            request,
            f'{updated} clearance request(s) approved successfully.'
        )

    @admin.action(description='Reject selected clearance requests')
    def reject_clearance(self, request, queryset):

        updated = queryset.update(
            status='REJECTED',
            reviewed_at=timezone.now(),
            approved_at=None,
        )

        self.message_user(
            request,
            f'{updated} clearance request(s) rejected.'
        )

    @admin.action(description='Mark selected requests as Under Review')
    def mark_under_review(self, request, queryset):

        updated = queryset.update(
            status='UNDER_REVIEW',
            reviewed_at=timezone.now(),
            approved_at=None,
        )

        self.message_user(
            request,
            f'{updated} clearance request(s) marked as under review.'
        )