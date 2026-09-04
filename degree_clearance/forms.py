from django import forms

from .models import DegreeClearance


class DegreeClearanceForm(forms.ModelForm):

    class Meta:
        model = DegreeClearance

        fields = [
            'remarks',
        ]

        widgets = {
            'remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': (
                        'Enter any additional information '
                        'for your degree clearance application...'
                    ),
                }
            ),
        }

        labels = {
            'remarks': 'Additional Information',
        }