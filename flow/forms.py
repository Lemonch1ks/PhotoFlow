from django import forms
from django.contrib.auth.forms import UserCreationForm

from flow.models import User, Booking


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email address')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = User.Role.CLIENT
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()

        return user


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking

        fields = [
            "service",
            "date",
            "start_time",
            "duration",
            "number_of_people",
            "comment",
        ]

        widgets = {
            "service": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "start_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),
            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 24,
                }
            ),
            "number_of_people": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your session requirements...",
                }
            ),
        }