from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from flow.views import (
    index,
    sign_up,
    studio_detail,
    studio_list,
    booking_list,
    book_session,
    service_list,
    photographer_list,
    photographer_detail,
)


app_name = "flow"

urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", sign_up, name="signup"),
    path("bookings/", booking_list, name="booking-list"),
    path("service_list/", service_list, name="service-list"),


    path(
        "studios/<int:studio_id>/",
        studio_detail,
        name="studio-detail",
    ),
    path(
        "studios/list/",
        studio_list,
        name="studio-list",
    ),
    path("studios/<int:pk>/book/", book_session, name="book-session"),
    path(
        "photographers/",
        photographer_list,
        name="photographer-list",
    ),
    path(
        "photographers/<int:pk>/",
        photographer_detail,
        name="photographer-detail",
    ),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
