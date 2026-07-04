from django.utils.text import slugify

def custom_slugify(value):
    slug = slugify(value)
    return slug.replace("-", "_")
