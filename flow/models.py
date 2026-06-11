from django.contrib.auth.models import AbstractUser
from django.db import models

from photoflow.settings import AUTH_USER_MODEL


class User(AbstractUser):
    role = models.CharField(max_length=100)
    pass


class StudioRoom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_hour = models.IntegerField()
    capacity = models.IntegerField()


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    duration = models.IntegerField()


class Booking(models.Model):
    client = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    photographer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    studio_room = models.ForeignKey(StudioRoom, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100)
    comment = models.TextField()
