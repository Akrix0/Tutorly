from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Currency(models.TextChoices):
    USD = "USD", "US Dollar"
    EUR = "EUR", "Euro"
    GBP = "GBP", "British Pound"
    JPY = "JPY", "Japanese Yen"
    HRN = "HRN", "Ukrainian Hryvnia"

class RatingField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 4)
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('validators', [MinValueValidator(0), MaxValueValidator(10)])
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        super().__init__(*args, **kwargs)
