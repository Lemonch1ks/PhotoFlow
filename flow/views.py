
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404

from flow.forms import SignUpForm, BookingForm
from flow.models import StudioRoom, User, Booking, Service


def index(request):
    context = {
        "studios": StudioRoom.objects.order_by("-id")[:3],
        "studio_room_count": StudioRoom.objects.all().count(),
        "photographers_count": User.objects.filter(role__icontains="photographer").count(),
        "session_count": Booking.objects.all().count(),
        "services": Service.objects.order_by("name")[:3],
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
    query = request.GET.get("q", "").strip()

    studios = StudioRoom.objects.all()

    if query:
        studios = studios.filter(name__icontains=query)

    paginator = Paginator(studios, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "studios": page_obj,
        "paginator": paginator,
        "page_obj": page_obj,
        "query": query,
    }

    return render(
        request,
        "photoflow/studio_list.html",
        context=context
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
    studio = get_object_or_404(
        StudioRoom,
        pk=pk,
    )
    if request.user.role == User.Role.CLIENT:

        if request.method == "POST":
            form = BookingForm(
                request.POST,
                studio=studio,
            )

            if form.is_valid():
                booking = form.save(commit=False)
                booking.client = request.user
                booking.studio_room = studio
                booking.status = "Pending"
                booking.duration = booking.service.duration
                booking.save()

                return redirect("flow:booking-list")
        else:
            form = BookingForm(studio=studio)

        return render(
            request,
            "photoflow/booking_session.html",
            {
                "studio": studio,
                "form": form,
            },
        )
    else:
        return render(
            request,
            "photoflow/error.html",
            context={
                "error_title": "No Permission",
                "error_message": "You cant create a booking for photo-session as a photographer",
            }
        )


def service_list(request):

    query = request.GET.get("q", "").strip()

    services = Service.objects.all().order_by("name")

    if query:
        services = services.filter(name__icontains=query)

    paginator = Paginator(services, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context ={
        "services": page_obj,
        "paginator": paginator,
        "page_obj": page_obj,
        "query": query,
    }

    return render(
        request,
        template_name="photoflow/service_list.html",
        context=context
    )


def photographer_list(request):
    query = request.GET.get("q", "").strip()

    photographers = User.objects.filter(role=User.Role.PHOTOGRAPHER).order_by("username")

    if query:
        photographers = photographers.filter(
            username__icontains=query
        )

    paginator = Paginator(photographers, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context ={
        "photographers": page_obj,
        "paginator": paginator,
        "page_obj": page_obj,
        "query": query,
    }
    return render(
        request,
        "photoflow/photograpger_list.html",
        context=context
    )


def photographer_detail(request, pk):
    photographer = get_object_or_404(
        User,
        pk=pk,
        role=User.Role.PHOTOGRAPHER,
    )

    return render(
        request,
        "photoflow/photograpger_detail.html",
        {
            "photographer": photographer,
        },
    )
