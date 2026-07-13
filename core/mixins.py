from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAnonymousMixin:
    """Allow access only to anonymous users."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You must be logged out to view this page.")
            return redirect("accounts:account_detail", slug=request.user.slug)
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
            return redirect("accounts:account_detail", slug=request.user.slug)
        return super().dispatch(request, *args, **kwargs)


class IsRequestUserMixin:
    """Allow access only to page's owner account."""

    def dispatch(self, request, *args, **kwargs):
        account = get_object_or_404(User, slug = kwargs["slug"])
        if account != request.user:
            messages.warning(request, "You can only access your own account page.")
            return redirect("accounts:account_detail", slug=request.user.slug)
        return super().dispatch(request, *args, **kwargs)
