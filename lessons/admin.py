from django.contrib import admin

from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "start_time",
        "end_time",
        "tutor",
        "student",
        "subject",
    )

    list_filter = (
        "date",
        "subject__subject",
    )

    search_fields = (
        "tutor__username",
        "student__username",
        "subject__subject__name",
    )

    autocomplete_fields = (
        "tutor",
        "student",
        "subject",
    )

    ordering = (
        "-date",
        "-start_time",
    )

    date_hierarchy = "date"

    list_select_related = (
        "tutor",
        "student",
        "subject",
        "subject__subject",
        "subject__tutor",
        "subject__tutor__account",
    )

    fieldsets = (
        (
            "Participants",
            {
                "fields": (
                    "tutor",
                    "student",
                    "subject",
                )
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "date",
                    ("start_time", "end_time"),
                )
            },
        ),
        (
            "Lesson",
            {
                "fields": (
                    "lesson_link",
                )
            },
        ),
    )