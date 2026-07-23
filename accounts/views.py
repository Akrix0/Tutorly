from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import Account
from core import mixins

class HomeTemplateView(TemplateView):
    template_name = "accounts/home.html"


class RegisterTemplateView(mixins.IsAnonymousMixin, TemplateView):
    template_name = "accounts/register.html"


class LoginTemplateView(mixins.IsAnonymousMixin, TemplateView):
    template_name = "accounts/login.html"


class LogoutTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/logout.html"

class AccountDetailView(TemplateView):
    template_name = "accounts/account_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Отримуємо акаунт, який треба показати
        account = get_object_or_404(Account, slug=self.kwargs.get("slug"))

        context["account"] = account
        context["account_is_tutor"] = account.is_tutor
        context["account_is_student"] = account.is_student
        
        user = self.request.user
        context["user_is_tutor"] = (
            user.is_authenticated and user.is_tutor
        )

        context["user_is_student"] = (
            user.is_authenticated and user.is_student
        )

        return context

class AccountEditView(mixins.IsRequestUserMixin, TemplateView):
    template_name = "accounts/account_edit.html"