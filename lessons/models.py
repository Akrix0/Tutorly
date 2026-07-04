from django.db import models
from django.core.exceptions import ValidationError

from core import exceptions
from core.models import BaseModel
from accounts.models import Account, TutorSubject

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
    
    def clean(self):
        super().clean()

        if self.tutor.role != Account.UserRole.TUTOR:
            raise exceptions.TutorRoleError()

        if self.student.role != Account.UserRole.STUDENT:
            raise exceptions.StudentRoleError()

        if self.start_time >= self.end_time:
            raise exceptions.InvalidTimeRangeError()
        
        if self.subject.tutor.account != self.tutor:
            raise ValidationError({
                "subject": "The selected subject does not belong to this tutor."
            })
        
    class Meta:
        ordering = [
            "-date",
            "-start_time",
        ]
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
