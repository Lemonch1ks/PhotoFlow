from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import datetime, timedelta
from flow.models import Booking, User
from django.db.models import Q


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email address",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
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

        fields = (
            "photographer",
            "service",
            "date",
            "start_time",
            "number_of_people",
            "comment",
        )

        widgets = {
            "photographer": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
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

    def __init__(self, *args, studio=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.studio = studio

        self.fields["photographer"].queryset = (
            User.objects
            .filter(role=User.Role.PHOTOGRAPHER)
            .order_by(
                "first_name",
                "last_name",
                "username",
            )
        )

        self.fields["photographer"].empty_label = (
            "Select a photographer"
        )

        self.fields["date"].widget.attrs["min"] = (
            timezone.localdate().isoformat()
        )

        if studio:
            self.fields["number_of_people"].widget.attrs[
                "max"
            ] = studio.capacity

    def clean_date(self):
        booking_date = self.cleaned_data["date"]

        if booking_date < timezone.localdate():
            raise forms.ValidationError(
                "The booking date cannot be in the past."
            )
        return booking_date

    def clean_number_of_people(self):
        number_of_people = self.cleaned_data[
            "number_of_people"
        ]

        if (
            self.studio
            and number_of_people > self.studio.capacity
        ):
            raise forms.ValidationError(
                f"This studio can accommodate a maximum "
                f"of {self.studio.capacity} people."
            )
        if number_of_people < 1:
            raise forms.ValidationError(
                "The number of people can not be less than one."
            )
        return number_of_people

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get("service")
        duration = service.duration if service else None
        photographer = cleaned_data.get("photographer")
        booking_date = cleaned_data.get("date")
        start_time = cleaned_data.get("start_time")
        if not all(
                (
                    photographer,
                    booking_date,
                    start_time,
                    duration,
                )
        ):
            return cleaned_data

        new_booking_start = datetime.combine(
            booking_date,
            start_time,
        )

        new_booking_end = new_booking_start + timedelta(
            minutes=duration,
        )

        existing_bookings = (
            Booking.objects
            .filter(date=booking_date)
            .exclude(status="Cancelled")
            .filter(
                Q(photographer=photographer)
                | Q(studio_room=self.studio)
            )
        )

        if self.instance.pk:
            existing_bookings = existing_bookings.exclude(
                pk=self.instance.pk,
            )

        for booking in existing_bookings:
            existing_booking_start = datetime.combine(
                booking.date,
                booking.start_time,
            )

            existing_booking_end = (
                existing_booking_start
                + timedelta(minutes=booking.duration)
            )

            has_time_conflict = (
                new_booking_start < existing_booking_end
                and new_booking_end > existing_booking_start
            )

            if has_time_conflict:
                raise forms.ValidationError(
                    "The selected photographer or studio is already "
                    "booked during this time."
                )

        return cleaned_data
