from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Subject


@receiver(post_migrate)
def create_subjects(sender, **kwargs):
    if sender.name != "accounts":
        return

    for value, _ in Subject.SubjectNames.choices:
        Subject.objects.get_or_create(name=value)