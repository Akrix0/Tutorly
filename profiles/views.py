from django.views.generic import TemplateView

from django_countries import countries

from .models import Subject, Availability
from core.models import Currency
from core import mixins


class TutorProfileCreateTemplateView(mixins.IsTutorMixin, mixins.HasNoTutorCardMixin, TemplateView):
    template_name = "profiles/tutor_profile_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["subjects"] = Subject.objects.all().order_by("name")
        context["currencies"] = Currency.choices
        context["weekdays"] = Availability.WeekDay.choices
        context["countries"] = list(countries)

        return context

class TutorProfileDetailTemplateView(mixins.IsTutorMixin, TemplateView):
    template_name = "profiles/tutor_profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_pk"] = self.kwargs["profile_pk"]
        return context