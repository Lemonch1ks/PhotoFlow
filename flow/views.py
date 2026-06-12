from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404

from flow.forms import SignUpForm
from flow.models import StudioRoom, User, Booking


def index(request):
    studios = StudioRoom.objects.all()
    context = {
        "studios": studios,
        "studio_room_count": StudioRoom.objects.all().count(),
        "photographers_count": User.objects.filter(role='Photographer').count(),
        "session_count": Booking.objects.all().count(),
    }


    return render(
        request,
        "photoflow/index.html",
        context=context,
    )


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("flow:index")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("flow:index")
    else:
        form = SignUpForm()

    return render(
        request,
        "registration/sign_up.html",
        {"form": form},
    )


def studio_detail(request, studio_id):
    studio = get_object_or_404(
        StudioRoom,
        id=studio_id,
    )

    return render(
        request,
        "photoflow/studio_detail.html",
        {
            "studio": studio,
        },
    )