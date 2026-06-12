from django.urls import path

from flow.views import index, sign_up, studio_detail


app_name = "flow"

urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", sign_up, name="signup"),

    path(
        "studios/<int:studio_id>/",
        studio_detail,
        name="studio-detail",
    ),
]