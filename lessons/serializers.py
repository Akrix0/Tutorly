from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Lesson
from profiles.models import Subject, TutorSubject

User = get_user_model()

class AccountShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]

class TutorSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = TutorSubject
        fields = ["id", "subject"]
class LessonReadSerializer(serializers.ModelSerializer):
    tutor = AccountShortSerializer(read_only=True)
    student = AccountShortSerializer(read_only=True)
    subject = TutorSubjectSerializer(read_only=True)

    display_subject_name = serializers.CharField(
        source="subject.subject_name",
        read_only=True,
    )

    display_date = serializers.DateField(
        source="date",
        format="%d.%m.%Y",
        read_only=True,
    )

    display_start_time = serializers.TimeField(
        source="start_time",
        format="%H:%M",
        read_only=True,
    )

    display_end_time = serializers.TimeField(
        source="end_time",
        format="%H:%M",
        read_only=True,
    )

    display_status = serializers.CharField(
        source="get_status_display",
        read_only=True
    )

    display_created_at = serializers.DateTimeField(
        source="created_at",
        format="%d.%m.%Y %H:%M",
        read_only=True,
    )

    display_updated_at = serializers.DateTimeField(
        source="updated_at",
        format="%d.%m.%Y %H:%M",
        read_only=True,
    )

    class Meta:
        model = Lesson
        fields = [
            "id",
            "tutor",
            "student",
            "subject",
            "date",
            "start_time",
            "end_time",
            "lesson_link",
            "status",
            "created_at",
            "updated_at",

            "display_subject_name",
            "display_date",
            "display_start_time",
            "display_end_time",
            "display_status",
            "display_created_at",
            "display_updated_at",
        ]

class LessonWriteSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.UserRole.STUDENT)
    )

    subject = serializers.PrimaryKeyRelatedField(
        queryset=TutorSubject.objects.none()
    )
    
    class Meta:
        model = Lesson
        fields = [
            "student",
            "subject",
            "date",
            "start_time",
            "end_time",
            "lesson_link",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["subject"].queryset = TutorSubject.objects.filter(
                tutor_card__account=request.user
            )