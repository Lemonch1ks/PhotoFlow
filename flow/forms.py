from django import forms
from django.contrib.auth.forms import UserCreationForm

from flow.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email address')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = User.Role.CLIENT
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()

        return user
