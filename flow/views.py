from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from flow.forms import SignUpForm, BookingSessionForm
from flow.models import StudioRoom, User, Booking


def index(request):
    studios = StudioRoom.objects.order_by("-id")[:3]
    context = {
        "studios": studios,
        "studio_room_count": StudioRoom.objects.all().count(),
        "photographers_count": User.objects.filter(role__icontains="photographer").count(),
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

def studio_list(request):
    studios = StudioRoom.objects.all()

    return render(
        request,
        "photoflow/studio_list.html",
        {
            "studios": studios,
        }
    )

@login_required
def booking_list(request):
    if request.user.role == User.Role.PHOTOGRAPHER:
        bookings = (
            request.user.photographer_bookings
            .select_related(
                "client",
                "studio_room",
                "service",
            )
            .order_by("-date", "-id")
        )

        page_title = "My photo session bookings"
    else:
        bookings = (
            request.user.client_bookings
            .select_related(
                "photographer",
                "studio_room",
                "service",
            )
            .order_by("-date", "-id")
        )

        page_title = "My bookings"

    return render(
        request,
        "photoflow/booking_list.html",
        {
            "bookings": bookings,
            "page_title": page_title,
        },
    )


@login_required
def book_session(request, pk):
    studio = get_object_or_404(StudioRoom, pk=pk)

    if request.method == "POST":
        form = BookingSessionForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.studio = studio
            booking.user = request.user
            booking.save()

            return redirect("studio-detail", pk=studio.pk)
    else:
        form = BookingSessionForm()

    return render(
        request,
        "photoflow/booking_session.html",
        {
            "studio": studio,
            "form": form,
        },
    )