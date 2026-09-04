from django.contrib import admin

from .models import FeeVoucher


@admin.register(FeeVoucher)
class FeeVoucherAdmin(admin.ModelAdmin):

    list_display = (
        'voucher_number',
        'student',
        'semester',
        'amount',
        'status',
        'due_date',
        'paid_date',
    )

    search_fields = (
        'voucher_number',
        'student__student_id',
        'student__registration_no',
        'student__user__first_name',
    )

    list_filter = (
        'status',
        'semester',
        'due_date',
    )

    ordering = (
        '-issue_date',
    )