from django.db.models.signals import post_save
from django.dispatch import receiver

from lessons.models import Lesson
from .models import Payment
from core import utils


@receiver(post_save, sender=Lesson)
def sync_payment_with_lesson(sender, instance, created, **kwargs):
    amount = utils.get_total_price(
        instance.subject.price_per_hour,
        instance.start_time,
        instance.end_time,
    )

    payment, _ = Payment.objects.get_or_create(
        lesson=instance,
        defaults={
            "amount": amount,
            "currency": instance.subject.currency,
        },
    )

    if not created:
        changed = False

        if payment.amount != amount:
            payment.amount = amount
            changed = True

        if payment.currency != instance.subject.currency:
            payment.currency = instance.subject.currency
            changed = True

        if changed:
            payment.save(update_fields=["amount", "currency"])