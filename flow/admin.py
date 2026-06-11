from django.contrib import admin

from flow.models import User, StudioRoom, Service, Booking

admin.site.register(User)
admin.site.register(StudioRoom)
admin.site.register(Service)
admin.site.register(Booking)

