from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    description = models.TextField(blank=True, null=True, default="")
