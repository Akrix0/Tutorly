from django.shortcuts import redirect
from django.contrib import messages

class IsAnonymousMixin:
    """Allow access only to anonymous users."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You must be logged out to view this page.")
            return redirect("profiles:tutor_profile_detail", profile_pk=request.user.tutor_card.pk)
        return super().dispatch(request, *args, **kwargs)

class IsTutorMixin:
    """Allow access only to tutors."""

    def dispatch(self, request, *args, **kwargs):
        if (not request.user.is_authenticated 
            or request.user.role != request.user.UserRole.TUTOR):
            messages.warning(request, "You must have tutor role to view this page.")
            return redirect("accounts:home")
        return super().dispatch(request, *args, **kwargs)

class HasNoTutorCardMixin:
    """Allow access only to tutors without a tutor card."""

    def dispatch(self, request, *args, **kwargs):
        tutor_card = getattr(request.user, "tutor_card", None)
        if tutor_card is not None:
            messages.warning(request, "You must not have tutor card to view this page.")
            return redirect("profiles:tutor_profile_detail", profile_pk=request.user.tutor_card.pk)
        return super().dispatch(request, *args, **kwargs)
