from django.db import models
from django.core.validators import MinValueValidator

from lessons.models import Lesson
from core.models import BaseModel, Currency

class Payment(BaseModel):
    class Providers(models.TextChoices):
        PAYPAL = "paypal", "PayPal"
        STRIPE = "stripe", "Stripe"
        MONOBANK = "monobank", "Monobank"
    
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"
        CANCELLED = "cancelled", "Cancelled"

    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(1)
        ], editable=False
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    provider = models.CharField(
        max_length=20,
        choices=Providers.choices,
        blank=True,
        null=True
    )
    provider_payment_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return (
            f"{self.lesson.student} → "
            f"{self.lesson.tutor} "
            f"({self.amount} {self.currency})"
        )

    class Meta:
        verbose_name="Payment"
        verbose_name_plural="Payments"