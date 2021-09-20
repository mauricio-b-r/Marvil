from django.db import models
from marvil.base import BaseModel


class Location(BaseModel):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    class Meta:
        db_table = "locations"
