from django.contrib.auth import login
from django.shortcuts import redirect, render

from flow.forms import SignUpForm


def index(request):
    return render(request, "photoflow/index.html")


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
