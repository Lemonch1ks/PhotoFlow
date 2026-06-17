
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from flow.forms import SignUpForm, BookingForm
from flow.models import StudioRoom, User, Booking, Service



class IndexView(generic.TemplateView):
    template_name = "photoflow/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["studios"] = StudioRoom.objects.order_by("-id")[:3]
        context["studio_room_count"] = int(StudioRoom.objects.all().count())
        context["photographers_count"] = int(User.objects.filter(
            role=User.Role.PHOTOGRAPHER
        ).count())
        context["session_count"] = int(Booking.objects.all().count())
        context["services"] = Service.objects.order_by("name")[:3]
        return context


class SignUpView(generic.FormView):
    template_name = "registration/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("flow:index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("flow:index")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)


class StudioDetailView(generic.DetailView):
    model = StudioRoom
    template_name = "photoflow/studio_detail.html"
    context_object_name = "studio"

    pk_url_kwarg = "studio_id"


class StudioListView(generic.ListView):
    model = StudioRoom
    template_name = "photoflow/studio_list.html"
    context_object_name = "studios"
    paginate_by = 6

    def get_queryset(self):
        queryset = StudioRoom.objects.order_by("name")

        query = self.request.GET.get("q", "").strip()

        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["query"] = self.request.GET.get("q", "").strip()

        return context


class BookingListView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = "photoflow/booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.PHOTOGRAPHER:
            return (
                user.photographer_bookings
                .select_related(
                    "client",
                    "studio_room",
                    "service",
                )
                .order_by("-date", "-id")
            )

        return (
            user.client_bookings
            .select_related(
                "photographer",
                "studio_room",
                "service",
            )
            .order_by("-date", "-id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.role == User.Role.PHOTOGRAPHER:
            context["page_title"] = "My photo session bookings"
        else:
            context["page_title"] = "My bookings"

        return context


class BookSessionView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView,
):
    model = Booking
    form_class = BookingForm
    template_name = "photoflow/booking_session.html"
    success_url = reverse_lazy("flow:booking-list")

    def dispatch(self, request, *args, **kwargs):
        self.studio = get_object_or_404(
            StudioRoom,
            pk=kwargs["pk"],
        )

        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.role == User.Role.CLIENT

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        return render(
            self.request,
            "photoflow/error.html",
            {
                "error_title": "No Permission",
                "error_message": (
                    "You cannot create a booking for a photo session "
                    "as a photographer."
                ),
            },
            status=403,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["studio"] = self.studio

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["studio"] = self.studio

        return context

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.studio_room = self.studio
        form.instance.status = "Pending"
        form.instance.duration = form.cleaned_data["service"].duration

        return super().form_valid(form)


class ServiceListView(generic.ListView):
    model = Service
    template_name = "photoflow/service_list.html"
    context_object_name = "services"
    paginate_by = 6

    def get_queryset(self):
        queryset = Service.objects.order_by("name")

        query = self.request.GET.get("q", "").strip()

        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["query"] = self.request.GET.get("q", "").strip()

        return context


class PhotographerListView(generic.ListView):
    model = User
    template_name = "photoflow/photograpger_list.html"
    context_object_name = "photographers"
    paginate_by = 6

    def get_queryset(self):
        queryset = User.objects.filter(
            role=User.Role.PHOTOGRAPHER,
        ).order_by("username")

        query = self.request.GET.get("q", "").strip()

        if query:
            queryset = queryset.filter(
                username__icontains=query,
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["query"] = self.request.GET.get("q", "").strip()

        return context


class PhotographerDetailView(generic.DetailView):
    model = User
    template_name = "photoflow/photograpger_detail.html"
    context_object_name = "photographer"

    def get_queryset(self):
        return User.objects.filter(
            role=User.Role.PHOTOGRAPHER,
        )
