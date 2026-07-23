from django.utils.text import slugify
from django.utils import timezone

from datetime import datetime
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken

from .exceptions import profiles

def custom_slugify(value):
    slug = slugify(value)
    return slug.replace("-", "_")

def get_total_price(price, start_time, end_time):
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)

    duration = Decimal((end_dt - start_dt).total_seconds()) / Decimal(3600)
    if duration <= 0:
        raise profiles.InvalidTimeRangeError()
    return round(price * duration, 2)

def find_average(*args):
    values = [v for v in args if v is not None]
    if not values:
        return None
    return round(sum(values) / len(values), 2)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_age(birth_date):
    today = timezone.now().date()
    if birth_date >= today:
        raise profiles.InvalidDataError("birth_date")
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age

def check_overlap(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1