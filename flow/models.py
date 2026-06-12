from django.contrib.auth.models import AbstractUser
from django.db import models

from photoflow import settings



class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        PHOTOGRAPHER = "photographer", "Photographer"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    def __str__(self):
        return self.username


class StudioRoom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_hour = models.IntegerField()
    capacity = models.IntegerField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.duration}"


class Booking(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_bookings",
    )

    photographer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="photographer_bookings",
    )

    studio_room = models.ForeignKey(StudioRoom, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100)
    comment = models.TextField()

    def __str__(self):
        return f"{self.studio_room.name} {self.service.name} {self.date}"

