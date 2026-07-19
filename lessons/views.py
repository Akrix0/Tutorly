from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from profiles.models import TutorSubject
from .models import Lesson
from core import mixins

User = get_user_model()

class LessonListView(LoginRequiredMixin, TemplateView):
    template_name = "lessons/lesson_list.html"

class LessonCreateView(mixins.IsTutorMixin, TemplateView):
    template_name = "lessons/lesson_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        account_slug = self.kwargs.get("slug")
        student_account = get_object_or_404(User, slug=account_slug)

        context["student"] = student_account
        context["subject"] = TutorSubject.objects.filter(
            tutor_card__account=self.request.user
        )

        return context

class LessonDetailView(LoginRequiredMixin, TemplateView):
    template_name = "lessons/lesson_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lesson_pk"] = self.kwargs["lesson_pk"]
        lesson = get_object_or_404(Lesson, id=context["lesson_pk"])
        context["lesson"] = lesson
        return context

class LessonEditView(LoginRequiredMixin, TemplateView):
    template_name = "lessons/lesson_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lesson_pk"] = self.kwargs["lesson_pk"]
        return context