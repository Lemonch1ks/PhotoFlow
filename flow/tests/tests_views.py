from datetime import timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from flow.forms import BookingForm
from flow.models import Service, StudioRoom, User, Booking


class SearchTests(TestCase):
    def test_search_studio_by_name(self):
        StudioRoom.objects.create(
            name="first_studio",
            price_per_hour=100,
            capacity=10,
        )

        StudioRoom.objects.create(
            name="another_studio",
            price_per_hour=50,
            capacity=12,
        )

        response = self.client.get(
            reverse("flow:studio-list"),
            data={"q": "first_studio"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "first_studio",)
        self.assertNotContains(response, "another_studio",)

    def test_search_service_by_name(self):
        Service.objects.create(
            name="first_service",
            price=100,
            description="first service",
            duration=10,
        )
        Service.objects.create(
            name="another_service",
            price=50,
            description="another service",
            duration=12,
        )
        response = self.client.get(
            reverse("flow:service-list"),
            data={"q": "first_service"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "first_service",)
        self.assertNotContains(response, "another_service",)

    def test_search_photographer_by_name(self):
        User.objects.create_user(
            role=User.Role.PHOTOGRAPHER,
            username="first_photographer",
            password="test_password",
        )

        User.objects.create_user(
            role=User.Role.PHOTOGRAPHER,
            username="another_photographer",
            password="test_password",
        )
        response = self.client.get(
            reverse("flow:photographer-list"),
            data={"q": "first"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "first_photographer",)
        self.assertNotContains(response, "another_photographer",)


class BookingTests(TestCase):
    def setUp(self):
        self.client_user = get_user_model().objects.create_user(
            username="client",
            password="Test_password_1234",
            role=User.Role.CLIENT,
        )
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
        self.another_photographer = get_user_model().objects.create_user(
            username="another_photographer",
            password="Test_password",
            role=User.Role.PHOTOGRAPHER,
        )

    def test_client_can_create_booking(self):

        booking_date = timezone.localdate() + timedelta(days=1)

        form = BookingForm(
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

        self.assertTrue(form.is_valid())

        booking = form.save(commit=False)
        booking.client = self.client_user
        booking.studio_room = self.studio
        booking.duration = self.service.duration
        booking.status = "Pending"
        booking.save()

        self.assertEqual(self.client_user, booking.client)
        self.assertEqual(self.studio, booking.studio_room)
        self.assertEqual(self.service, booking.service)
        self.assertEqual(self.photographer, booking.photographer)

    def test_photographer_cannot_create_booking(self):
        self.client.force_login(self.photographer)

        booking_date = timezone.localdate() + timedelta(days=1)

        response = self.client.post(
            reverse(
                "flow:book-session",
                kwargs={"pk": self.studio.pk},
            ),
            data={
                "photographer": self.photographer.pk,
                "service": self.service.pk,
                "date": booking_date.isoformat(),
                "start_time": "10:00",
                "number_of_people": 2,
                "comment": "",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "photoflow/error.html",
        )

        self.assertContains(
            response,
            "You cant create a booking for photo-session as a photographer",
        )

        self.assertEqual(
            Booking.objects.count(),
            0,
        )
