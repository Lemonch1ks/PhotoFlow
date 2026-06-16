from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from flow.forms import BookingForm
from flow.models import Service, StudioRoom, User


class BookingFormTests(TestCase):
    def setUp(self):
        self.photographer = get_user_model().objects.create_user(
            username="photographer",
            password="Test_password_1234",
            role=User.Role.PHOTOGRAPHER,
        )

        self.studio = StudioRoom.objects.create(
            name="Test studio",
            price_per_hour=100,
            capacity=10,
        )

        self.service = Service.objects.create(
            name="Portrait session",
            description="Test service",
            price=100,
            duration=60,
        )

        self.client_user = get_user_model().objects.create_user(
            username="client",
            password="Test_password_1234",
            role=User.Role.CLIENT,
        )

    def test_booking_date_cannot_be_in_past(self):
        past_date = timezone.localdate() - timedelta(days=1)

        form = BookingForm(
            data={
                "photographer": self.photographer.pk,
                "service": self.service.pk,
                "date": past_date.isoformat(),
                "start_time": "10:00",
                "number_of_people": 1,
                "comment": "",
            },
            studio=self.studio,
        )

        self.assertFalse(form.is_valid())

        self.assertFormError(
            form,
            "date",
            "The booking date cannot be in the past.",
        )

    def test_number_of_people_cannot_exceed_studio_capacity(self):
        form = BookingForm(
            data={
                "photographer": self.photographer.pk,
                "service": self.service.pk,
                "date": timezone.localdate() + timedelta(days=1),
                "start_time": "10:00",
                "number_of_people": 212,
                "comment": "",
            },
            studio=self.studio,
        )
        self.assertFalse(form.is_valid())

    def test_booking_conflict_for_same_photographer(self):
        booking_date = timezone.localdate() + timedelta(days=1)

        second_studio = StudioRoom.objects.create(
            name="Second studio",
            price_per_hour=150,
            capacity=10,
        )

        form1 = BookingForm(
            data={
                "photographer": self.photographer.pk,
                "service": self.service.pk,
                "date": booking_date.isoformat(),
                "start_time": "10:00",
                "number_of_people": 2,
                "comment": "",
            },
            studio=self.studio,
        )

        self.assertTrue(form1.is_valid())

        booking = form1.save(commit=False)
        booking.client = self.client_user
        booking.studio_room = self.studio
        booking.duration = self.service.duration
        booking.status = "Pending"
        booking.save()

        form2 = BookingForm(
            data={
                "photographer": self.photographer.pk,
                "service": self.service.pk,
                "date": booking_date.isoformat(),
                "start_time": "10:00",
                "number_of_people": 2,
                "comment": "",
            },
            studio=second_studio,
        )

        self.assertFalse(form2.is_valid())
