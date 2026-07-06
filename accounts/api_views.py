from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from core.utils import get_tokens_for_user

@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(APIView):
    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = authenticate(request=request, **serializer.validated_data)
        if user:
            login(request, user)
            token = get_tokens_for_user(user)
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