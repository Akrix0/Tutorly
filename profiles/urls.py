from django.urls import path
from . import views, api_views

app_name = "profiles"

urlpatterns = [
    path("profile/create/", views.TutorProfileCreateTemplateView.as_view(), name="tutor_profile_create"),
    
    # API
    path("api/profile/create/", api_views.TutorProfileCreateView.as_view(), name="tutor_profile_create_api"),
]