from django.contrib import admin

from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
    )

    ordering = ("username",)