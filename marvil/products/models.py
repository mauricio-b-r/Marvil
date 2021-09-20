from django.db import models
from marvil.base import BaseModel
from locations.models import Location


class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"


class Brand(BaseModel):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, related_name="brands", null=True
    )

    class Meta:
        db_table = "brands"


class Product(BaseModel):
    STORED_IN_WAREHOUSE = "warehouse"
    STORED_IN_SHOPWINDOW = "shopwindow"
    STORED_IN_HOME = "home"

    STORED_IN_CHOICES = (
        (STORED_IN_WAREHOUSE, "Stored in the warehouse"),
        (STORED_IN_SHOPWINDOW,  "Stored in shopwindow"),
        (STORED_IN_HOME,  "Stored in home")
    )
    description = models.TextField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    stored_in = models.CharField(choices=STORED_IN_CHOICES, max_length=50)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")

    class Meta:
        db_table = "products"
