from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . import serializers, models
from core import permissions

class TutorProfileCreateView(APIView):
    permission_classes = [IsAuthenticated, permissions.HasNoTutorCard, permissions.IsTutor]

    def post(self, request):
        serializer = serializers.TutorProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(account=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TutorProfileDetailView(APIView):
    permission_classes = [IsAuthenticated, permissions.IsTutor]

    def get(self, request, profile_pk):
        profile = get_object_or_404(models.TutorCard, pk=profile_pk)
        serializer = serializers.TutorProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)