from django import forms
from .models import ExamForm


class ExamFormCreateForm(forms.ModelForm):

    class Meta:
        model = ExamForm
        fields = [
            'exam_type',
            'academic_session',
            'semester',
        ]

        widgets = {
            'exam_type': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'academic_session': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '2026-2027'
                }
            ),

            'semester': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1
                }
            ),
        }