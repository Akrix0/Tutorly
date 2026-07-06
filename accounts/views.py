from django.views.generic import TemplateView


class RegisterTemplateView(TemplateView):
    template_name = "accounts/register.html"


class LoginTemplateView(TemplateView):
    template_name = "accounts/login.html"


class LogoutTemplateView(TemplateView):
    template_name = "accounts/logout.html"