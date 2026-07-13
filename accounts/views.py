from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core import mixins

class HomeTemplateView(TemplateView):
    template_name = "accounts/home.html"


class RegisterTemplateView(mixins.IsAnonymousMixin, TemplateView):
    template_name = "accounts/register.html"


class LoginTemplateView(mixins.IsAnonymousMixin, TemplateView):
    template_name = "accounts/login.html"


class LogoutTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/logout.html"


class AccountDetailView(mixins.IsRequestUserMixin, TemplateView):
    template_name = "accounts/account_detail.html"


class AccountEditView(mixins.IsRequestUserMixin, TemplateView):
    template_name = "accounts/account_edit.html"