from django.utils.text import slugify

from datetime import datetime

from .exceptions import InvalidTimeRangeError

def custom_slugify(value):
    slug = slugify(value)
    return slug.replace("-", "_")

def get_total_price(price, start_time, end_time):
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)

    duration = (end_dt - start_dt).total_seconds() / 3600
    if duration <= 0:
        raise InvalidTimeRangeError()
    return round(price * duration, 2)