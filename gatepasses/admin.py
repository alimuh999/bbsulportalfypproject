from django.contrib import admin
from django.utils import timezone

from .models import GatePass


@admin.action(description='Approve selected gate passes')
def approve_gate_passes(modeladmin, request, queryset):
    updated_count = queryset.update(
        status='APPROVED',
        admin_remarks='Approved by administration.',
    )

    modeladmin.message_user(
        request,
        f'{updated_count} gate pass(es) approved successfully.'
    )


@admin.action(description='Reject selected gate passes')
def reject_gate_passes(modeladmin, request, queryset):
    updated_count = queryset.update(
        status='REJECTED',
        admin_remarks='Rejected by administration.',
    )

    modeladmin.message_user(
        request,
        f'{updated_count} gate pass(es) rejected.'
    )


@admin.action(description='Mark selected gate passes as Pending')
def mark_pending_gate_passes(modeladmin, request, queryset):
    updated_count = queryset.update(
        status='PENDING',
        admin_remarks='',
    )

    modeladmin.message_user(
        request,
        f'{updated_count} gate pass(es) marked as pending.'
    )


@admin.register(GatePass)
class GatePassAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'departure_date',
        'departure_time',
        'return_date',
        'return_time',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'departure_date',
        'return_date',
    )

    search_fields = (
        'student__student_id',
        'student__user__first_name',
        'student__user__last_name',
        'reason',
    )

    readonly_fields = ('created_at',)

    actions = [
        approve_gate_passes,
        reject_gate_passes,
        mark_pending_gate_passes,
    ]