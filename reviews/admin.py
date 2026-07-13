from django.contrib import admin
from .models import Review, Rating


class RatingInline(admin.StackedInline):
    model = Rating
    extra = 0
    max_num = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "lesson",
        "student",
        "tutor",
        "created_at",
    )
    search_fields = (
        "lesson__student__username",
        "lesson__tutor__username",
        "lesson__subject__subject__name",
    )
    list_filter = (
        "lesson__status",
        "created_at",
    )
    ordering = ("-created_at",)
    autocomplete_fields = ("lesson",)
    inlines = (RatingInline,)
    readonly_fields = (
        "created_at",
        "updated_at",
        "student",
        "tutor",
    )
    fieldsets = (
        (
            "Review",
            {
                "fields": (
                    "lesson",
                    "student",
                    "tutor",
                    "message",
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

    @admin.display(ordering="lesson__student__username")
    def student(self, obj):
        return obj.student.username

    @admin.display(ordering="lesson__tutor__username")
    def tutor(self, obj):
        return obj.tutor.username


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "review",
        "average",
        "explanation",
        "communication",
        "materials",
        "organization",
        "individual_approach",
    )
    search_fields = (
        "review__lesson__student__username",
        "review__lesson__tutor__username",
    )
    autocomplete_fields = ("review",)
    readonly_fields = (
        "average",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Rating",
            {
                "fields": (
                    "review",
                    "explanation",
                    "communication",
                    "materials",
                    "organization",
                    "individual_approach",
                    "average",
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
