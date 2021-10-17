from decimal import ROUND_UP, Decimal

from django.db import models
from locations.models import Location
from marvil.base import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator


def update_qs_decimal_field(number, field, qs):
    decimal_number = Decimal(number)
    dct = {f"{field}": (models.F(field) + decimal_number)}
    qs.update(**dct)


class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def update_products_price(self, amount):
        update_qs_decimal_field(amount, "price", self.products)

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"


class Brand(BaseModel):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, related_name="brands", null=True
    )

    def update_products_price(self, amount):
        update_qs_decimal_field(amount, "price", self.products)

    class Meta:
        db_table = "brands"


class Discount(BaseModel):
    # Cron for updating discounts
    amount = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    date_from = models.DateTimeField(blank=True, null=True)
    date_to = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "discounts"


class Product(BaseModel):
    STORED_IN_WAREHOUSE = "warehouse"
    STORED_IN_SHOPWINDOW = "shopwindow"
    STORED_IN_HOME = "home"

    STORED_IN_CHOICES = (
        (STORED_IN_WAREHOUSE, "Stored in the warehouse"),
        (STORED_IN_SHOPWINDOW, "Stored in shopwindow"),
        (STORED_IN_HOME, "Stored in home"),
    )
    description = models.TextField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    stored_in = models.CharField(choices=STORED_IN_CHOICES, max_length=50)
    is_archived = models.BooleanField(default=False)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )

    def get_price_with_discounts(self):
        discounts = self.discounts.filter(is_active=True).annotate(
            totals=models.Sum("amount")
        )["totals"]
        return Decimal(self.price * (100 - discounts) / 100).quantize(
            Decimal("0.01"), rounding=ROUND_UP
        )

    class Meta:
        db_table = "products"
        permissions = [
            ("Can update the discounts", "can_update_discounts"),
            ("Can update product", "can_update_product"),
            ("Can create product", "can_create_product"),
            ("Can archive product", "can_archive_product"),
        ]
