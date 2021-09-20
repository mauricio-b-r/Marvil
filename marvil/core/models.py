from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, help_text="Who are you?")
    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
    )
    birth_date = models.DateField(null=True, blank=True)
