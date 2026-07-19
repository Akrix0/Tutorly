from django.db import models

from core.exceptions import profiles, lessons
from core.models import BaseModel
from accounts.models import Account
from profiles.models import TutorSubject

from datetime import datetime
from django.utils import timezone


class Lesson(BaseModel):
    class LessonStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
    tutor = models.ForeignKey(Account, on_delete=models.PROTECT , related_name="tutor_lessons")
    student = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="student_lessons")
    subject = models.ForeignKey(TutorSubject, on_delete=models.CASCADE, related_name="subject_lessons")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    lesson_link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=LessonStatus.choices, default=LessonStatus.PENDING)

    def __str__(self):
        return f"{self.subject} with {self.tutor.username} for {self.student.username} on {self.date}"
    
    @property
    def title(self):
        return f"{self.subject.subject_name} Lesson for {self.student.username} with {self.tutor.username}"
    
    def clean(self):
        super().clean()

        if self.tutor.role != Account.UserRole.TUTOR:
            raise profiles.TutorRoleError()

        if self.student.role != Account.UserRole.STUDENT:
            raise profiles.StudentRoleError()

        if self.start_time >= self.end_time:
            raise profiles.InvalidTimeRangeError()
        
        if self.subject.tutor_card.account != self.tutor:
            raise profiles.NotTutorSubjectError()
        
        lesson_datetime = timezone.make_aware(
            datetime.combine(self.date, self.start_time)
        )

        if lesson_datetime < timezone.now():
            raise profiles.LessonInPastError()
        
        has_availability = self.tutor.tutor_card.availabilities.filter(
            weekday=self.date.isoweekday(),
            start_time__lte=self.start_time,
            end_time__gte=self.end_time,
        ).exists()

        if not has_availability:
            raise profiles.TutorNotAvailableError()

        has_conflict = Lesson.objects.filter(
            tutor=self.tutor,
            date=self.date,
        ).exclude(
            pk=self.pk,
        ).filter(
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exists()

        if has_conflict:
            raise lessons.LessonTimeConflictError()
        
    class Meta:
        ordering = [
            "-date",
            "-start_time",
        ]
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
