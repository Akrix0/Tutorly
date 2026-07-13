from rest_framework.permissions import BasePermission
from profiles.models import TutorCard

class IsAnonymous(BasePermission):
    message = "You are already authenticated."

    def has_permission(self, request, view):
        return not request.user.is_authenticated

class IsTutor(BasePermission):
    message = "Only tutors can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == request.user.UserRole.TUTOR
        )

class HasNoTutorCard(BasePermission):
    message = "One tutor card per tutor."

    def has_permission(self, request, view):
        return not hasattr(request.user, "tutor_card")

class IsRequestUser(BasePermission):
    message = "Only owner can enter their account page."

    def has_object_permission(self, request, view, obj):
        return obj == request.user