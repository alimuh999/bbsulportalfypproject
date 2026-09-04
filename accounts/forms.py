from django import forms
from django.contrib.auth.models import User
from .models import Student


# ==========================================
# STUDENT CREATION FORM
# ==========================================

class StudentCreationForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        label="Student Login ID"
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )

    first_name = forms.CharField(
        max_length=150,
        label="Student Name"
    )

    email = forms.EmailField(
        required=False
    )

    class Meta:
        model = Student

        fields = [
            'student_id',
            'registration_no',
            'father_name',
            'department',
            'program',
            'semester',
            'section',
            'phone',
            'address',
            'gender',
            'date_of_birth',
            'profile_picture',
            'fee_status',
        ]

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This Student Login ID already exists."
            )

        return username

    def save(self, commit=True):

        student = super().save(commit=False)

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        first_name = self.cleaned_data['first_name']
        email = self.cleaned_data['email']

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            email=email
        )

        student.user = user

        if commit:
            student.save()

        return student


# ==========================================
# STUDENT PROFILE EDIT FORM
# ==========================================

class StudentProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=150,
        label="Student Name"
    )

    email = forms.EmailField(
        required=False,
        label="Email"
    )

    class Meta:
        model = Student

        fields = [
            'first_name',
            'email',
            'phone',
            'address',
            'date_of_birth',
            'profile_picture',
        ]

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):

        student = super().save(commit=False)

        user = student.user

        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            student.save()

        return student