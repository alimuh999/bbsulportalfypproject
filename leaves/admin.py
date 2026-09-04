from django.contrib import admin
from django.utils import timezone

from .models import LeaveRequest


@admin.action(description='Mark selected requests as Under Review')
def mark_under_review(modeladmin, request, queryset):

    updated_count = queryset.update(
        status='UNDER_REVIEW'
    )

    modeladmin.message_user(
        request,
        f'{updated_count} leave request(s) marked as under review.'
    )


@admin.action(description='Approve selected leave requests')
def approve_leave_requests(modeladmin, request, queryset):

    updated_count = queryset.update(
        status='APPROVED',
        reviewed_at=timezone.now()
    )

    modeladmin.message_user(
        request,
        f'{updated_count} leave request(s) approved successfully.'
    )


@admin.action(description='Reject selected leave requests')
def reject_leave_requests(modeladmin, request, queryset):

    updated_count = queryset.update(
        status='REJECTED',
        admin_remarks='Rejected by administration.',
        reviewed_at=timezone.now()
    )

    modeladmin.message_user(
        request,
        f'{updated_count} leave request(s) rejected.'
    )


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'leave_type',
        'start_date',
        'end_date',
        'status',
        'submitted_at',
        'reviewed_at',
    )

    list_filter = (
        'leave_type',
        'status',
        'start_date',
    )

    search_fields = (
        'student__student_id',
        'student__user__first_name',
        'student__user__last_name',
        'reason',
    )

    readonly_fields = (
        'submitted_at',
        'reviewed_at',
    )

    actions = [
        mark_under_review,
        approve_leave_requests,
        reject_leave_requests,
    ]