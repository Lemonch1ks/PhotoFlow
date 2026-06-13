from django.urls import path

from flow.views import (
    index,
    sign_up,
    studio_detail,
    studio_list,
    booking_list,
    book_session,
)


app_name = "flow"

urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", sign_up, name="signup"),
    path("bookings/", booking_list, name="booking-list"),

    path(
        "studios/<int:studio_id>/",
        studio_detail,
        name="studio-detail",
    ),
    path(
        "studios/list",
        studio_list,
        name="studio-list",
    ),
    path(
    "studios/<int:pk>/book/",
    book_session,
    name="book-session",
    ),
]