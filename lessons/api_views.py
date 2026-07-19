from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Lesson
from core import permissions 

User = get_user_model()

class LessonViewSet(ModelViewSet):

    def get_permissions(self):
        if self.action not in ["list", "retrieve"]:
            return [
                IsAuthenticated(),
                permissions.IsTutor(),
            ]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.UserRole.TUTOR:
            return Lesson.objects.filter(tutor=user)
        
        if user.role == User.UserRole.STUDENT:
            return Lesson.objects.filter(student=user)
        
        if user.role == User.UserRole.ADMIN:
            return Lesson.objects.all()
        
        return Lesson.objects.none()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.LessonReadSerializer
        return serializers.LessonWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson = serializer.save(tutor=request.user)

        return Response(
            serializers.LessonReadSerializer(
                lesson,
                context=self.get_serializer_context()
            ).data,
            status=status.HTTP_201_CREATED,
        )