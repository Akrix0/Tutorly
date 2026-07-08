from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . import serializers
from accounts.models import Account
from core import exceptions

class TutorProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != Account.UserRole.TUTOR:
            raise exceptions.TutorRoleError()

        serializer = serializers.TutorProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(account=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
