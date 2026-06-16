from datetime import timedelta, time
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase

from flow.models import Service, StudioRoom, User, Booking


class ModelTest(TestCase):
    def test_studio_room_str(self):
        studio = StudioRoom.objects.create(
            name="White Studio",
            price_per_hour=100,
            capacity=10,
        )

        self.assertEqual(str(studio), "White Studio")

    def test_service_str(self):
        service = Service.objects.create(
            name="White Service",
            price=100,
            duration=120
        )
        self.assertEqual(str(service), "White Service 120")

    def test_booking_str(self):
        booking_date = timezone.localdate() + timedelta(days=1)

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
        booking = Booking.objects.create(
            client=self.client_user,
            photographer=self.photographer,
            studio_room=self.studio,
            service=self.service,
            start_time=time(0, 0),
            date=booking_date,
            duration=60,
            number_of_people=3,
        )
        self.assertEqual(
            str(booking),
            f"Test studio Portrait session {booking_date}"
        )
