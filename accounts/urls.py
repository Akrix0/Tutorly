from django.urls import path
from . import views, api_views

app_name = "accounts"

urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name="home"),
    path("register/", views.RegisterTemplateView.as_view(), name="register"),
    path("login/", views.LoginTemplateView.as_view(), name="login"),
    path("logout/", views.LogoutTemplateView.as_view(), name="logout"),
    path("<slug:slug>/", views.AccountDetailView.as_view(), name="account_detail"),
    path("update/<slug:slug>/", views.AccountEditView.as_view(), name="account_edit"),

    # API
    path("api/register/", api_views.RegisterView.as_view(), name="register_api"),
    path("api/login/", api_views.LoginView.as_view(), name="login_api"),
    path("api/logout/", api_views.LogoutView.as_view(), name="logout_api"),
    path("api/<slug:slug>/", api_views.Account.as_view(), name="account_api")
]