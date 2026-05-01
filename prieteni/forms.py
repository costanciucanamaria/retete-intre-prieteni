from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import  CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "description")

