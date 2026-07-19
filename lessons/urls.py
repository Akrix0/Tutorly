from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import LessonViewSet

app_name = "lessons"

router = DefaultRouter()
router.register("", LessonViewSet, basename="lesson")

urlpatterns = [
    path("", views.LessonListView.as_view(), name="lesson_list"),
    path("create/<slug:slug>/", views.LessonCreateView.as_view(), name="lesson_create"),
    path("<int:lesson_pk>/", views.LessonDetailView.as_view(), name="lesson_detail"),
    path("<int:lesson_pk>/edit/", views.LessonEditView.as_view(), name="lesson_edit"),

    # API
    path("api/", include(router.urls)),
]
