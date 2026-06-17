from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from flow.views import (
    IndexView,
    SignUpView,
    StudioDetailView,
    StudioListView,
    BookingListView,
    BookSessionView,
    ServiceListView,
    PhotographerListView,
    PhotographerDetailView,
)


app_name = "flow"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("sign-up/", SignUpView.as_view(), name="signup"),
    path("bookings/", BookingListView.as_view(), name="booking-list"),
    path("service_list/", ServiceListView.as_view(), name="service-list"),


    path(
        "studios/<int:studio_id>/",
        StudioDetailView.as_view(),
        name="studio-detail",
    ),
    path(
        "studios/list/",
        StudioListView.as_view(),
        name="studio-list",
    ),
    path("studios/<int:pk>/book/", BookSessionView.as_view(), name="book-session"),
    path(
        "photographers/",
        PhotographerListView.as_view(),
        name="photographer-list",
    ),
    path(
        "photographers/<int:pk>/",
        PhotographerDetailView.as_view(),
        name="photographer-detail",
    ),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
