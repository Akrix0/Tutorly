from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . import serializers
from core import utils, permissions 

User = get_user_model()

@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(APIView):
    permission_classes = [permissions.IsAnonymous]

    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    permission_classes = [permissions.IsAnonymous]
    
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = authenticate(request=request, **serializer.validated_data)
        if user:
            login(request, user)
            token = utils.get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    def post(self, request):
        serializer = serializers.UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logout(request)
        token = serializer.validated_data["token"]
        token.blacklist()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class Account(APIView):
    permission_classes = [IsAuthenticated, permissions.IsRequestUser]

    def get(self, request, slug):
        account = get_object_or_404(User, slug=slug)
        self.check_object_permissions(request, account)
        serializer = serializers.AccountSerializer(account)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        account = get_object_or_404(User, slug=slug)
        self.check_object_permissions(request, account)
        serializer = serializers.AccountSerializer(instance=account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
