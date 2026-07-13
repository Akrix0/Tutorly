from django import forms
from django.contrib import admin

from accounts.models import Account
from .models import Subject, TutorCard, TutorSubject, Availability



class TutorSubjectInline(admin.TabularInline):
    model = TutorSubject
    extra = 1
    autocomplete_fields = ("subject",)


class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1


class TutorCardAdminForm(forms.ModelForm):
    class Meta:
        model = TutorCard
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Показуємо лише акаунти репетиторів
        self.fields["account"].queryset = Account.objects.filter(
            role=Account.UserRole.TUTOR
        )

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TutorCard)
class TutorCardAdmin(admin.ModelAdmin):
    form = TutorCardAdminForm

    list_display = (
        "account",
        "country",
        "experience_years",
    )

    search_fields = (
        "account__username",
        "account__email",
    )

    list_filter = (
        "country",
    )

    autocomplete_fields = (
        "account",
    )

    inlines = (
        TutorSubjectInline,
        AvailabilityInline,
    )


@admin.register(TutorSubject)
class TutorSubjectAdmin(admin.ModelAdmin):
    list_display = (
        "tutor_card",
        "subject",
        "price_per_hour",
    )

    list_filter = (
        "subject",
    )

    search_fields = (
        "tutor_card__account__username",
        "subject__name",
    )

    autocomplete_fields = (
        "tutor_card",
        "subject",
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "tutor_card",
        "weekday",
        "start_time",
        "end_time",
    )

    list_filter = (
        "weekday",
    )

    search_fields = (
        "tutor_card__account__username",
    )

    autocomplete_fields = (
        "tutor_card",
    )