from django.contrib import admin

from flow.models import User, StudioRoom, Service, Booking

admin.site.register(StudioRoom)
admin.site.register(Service)
admin.site.register(Booking)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'role'
    )
    list_filter = (
        'role',
    )
    search_fields = (
        'username',
    )
