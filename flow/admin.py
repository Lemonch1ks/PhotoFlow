from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from flow.models import User, StudioRoom, Service, Booking


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

@admin.register(StudioRoom)
class StudioRoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price_per_hour",
        'capacity',
        "image",
        'description'
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = ("name",)

    list_filter = (
        "capacity",
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "duration_in_hours",
        "description",
    )

    list_filter = (
        "price",
    )

    @admin.display(description="Duration", ordering="duration")
    def duration_in_hours(self, obj):
        unit = "hour" if obj.duration == 1 else "hours"
        return f"{obj.duration} {unit}"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "date",
        "photographer",
        "status",
        "studio_room",
        "start_time",
        "number_of_people",
        "duration",
    )

    list_filter = (
        "client",
        "date",
        "photographer",
        "status",
        "studio_room",
    )

    fieldsets = [
        (
            None,
            {
                "fields": ["client", "photographer","date", "studio_room", "service", "status", "comment", "duration", "start_time", "number_of_people"],
            }
        )
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "photographer":
            kwargs["queryset"] = User.objects.filter(
                role=User.Role.PHOTOGRAPHER,
            )

        elif db_field.name == "client":
            kwargs["queryset"] = User.objects.filter(
                role=User.Role.CLIENT,
            )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )
