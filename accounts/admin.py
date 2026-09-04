from django.contrib import admin
from .models import Student
from .forms import StudentCreationForm


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'student_id',
        'registration_no',
        'get_name',
        'department',
        'program',
        'semester',
        'fee_status',
    )

    search_fields = (
        'student_id',
        'registration_no',
        'user__first_name',
        'user__last_name',
    )

    list_filter = (
        'department',
        'program',
        'semester',
        'fee_status',
    )

    def get_form(self, request, obj=None, **kwargs):

        if obj is None:
            return StudentCreationForm

        return super().get_form(request, obj, **kwargs)

    def get_name(self, obj):
        return obj.user.get_full_name()

    get_name.short_description = 'Student Name'