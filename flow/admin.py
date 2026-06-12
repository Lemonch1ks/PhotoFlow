from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from flow.models import User, StudioRoom, Service, Booking

admin.site.register(StudioRoom)
admin.site.register(Service)
admin.site.register(Booking)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
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
        "username",
        "first_name",
        "last_name",
        "email",
    )

    ordering = (
        "username",
    )

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional information",
            {
                "fields": (
                    "role",
                ),
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Personal information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "role",
                ),
            },
        ),
    )