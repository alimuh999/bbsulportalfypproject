from django import forms
from .models import GatePass


class GatePassForm(forms.ModelForm):
    class Meta:
        model = GatePass
        fields = [
            'reason',
            'departure_date',
            'departure_time',
            'return_date',
            'return_time',
        ]

        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Gate pass ki wajah likhein'
            }),

            'departure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'departure_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),

            'return_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'return_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        departure_date = cleaned_data.get('departure_date')
        return_date = cleaned_data.get('return_date')

        if departure_date and return_date:
            if return_date < departure_date:
                raise forms.ValidationError(
                    'Return date departure date se pehle nahi ho sakti.'
                )

        return cleaned_data