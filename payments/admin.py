from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "lesson",
        "amount",
        "currency",
        "status",
        "provider",
        "paid_at",
        "created_at",
    )

    list_filter = (
        "status",
        "provider",
        "currency",
        "created_at",
        "paid_at",
    )

    search_fields = (
        "lesson__student__username",
        "lesson__tutor__username",
        "provider_payment_id",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "amount",
        "currency",
        "provider_payment_id",
        "paid_at",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("lesson",)

    fieldsets = (
        (
            "Payment Information",
            {
                "fields": (
                    "lesson",
                    "amount",
                    "currency",
                )
            },
        ),
        (
            "Provider",
            {
                "fields": (
                    "provider",
                    "provider_payment_id",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "paid_at",
                )
            },
        ),
        (
            "System",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )