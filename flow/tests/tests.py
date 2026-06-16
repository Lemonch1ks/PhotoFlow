from django.test import TestCase
from django.urls import reverse

from flow.models import StudioRoom, Service, User


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
