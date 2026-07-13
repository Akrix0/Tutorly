from django.urls import path
from . import views, api_views

app_name = "profiles"

urlpatterns = [
    path("profile/create/", views.TutorProfileCreateTemplateView.as_view(), name="tutor_profile_create"),
    path("profile/<int:profile_pk>/", views.TutorProfileDetailTemplateView.as_view(), name="tutor_profile_detail"),

    # API
    path("api/profile/create/", api_views.TutorProfileCreateView.as_view(), name="tutor_profile_create_api"),
    path('api/profile/<int:profile_pk>/', api_views.TutorProfileDetailView.as_view(), name="tutor_profile_detail_api"),
]