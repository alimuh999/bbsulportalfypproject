from django.contrib import admin
from .models import Result, Marksheet


# ==========================================
# RESULT ADMIN
# ==========================================

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'semester',
        'subject_code',
        'subject_name',
        'credit_hours',
        'obtained_marks',
        'total_marks',
        'get_percentage',
        'get_grade',
    )

    list_filter = (
        'semester',
    )

    search_fields = (
        'student__student_id',
        'student__registration_no',
        'subject_name',
        'subject_code',
    )

    def get_percentage(self, obj):
        return f"{obj.percentage()}%"

    get_percentage.short_description = 'Percentage'

    def get_grade(self, obj):
        return obj.grade()

    get_grade.short_description = 'Grade'


# ==========================================
# MARKSHEET ADMIN
# ==========================================

@admin.register(Marksheet)
class MarksheetAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'semester',
        'issue_date',
        'is_published',
    )

    list_filter = (
        'semester',
        'is_published',
    )

    search_fields = (
        'student__student_id',
        'student__registration_no',
        'student__user__first_name',
        'student__user__last_name',
    )

    list_editable = (
        'is_published',
    )