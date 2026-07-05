from django.db import models

from lessons.models import Lesson
from core import exceptions
from core.models import BaseModel, RatingField
from core.utils import find_average

class Review(BaseModel):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name="review")
    message = models.TextField(blank=True)
    
    def clean(self):
        super().clean()

        if self.lesson.status != Lesson.LessonStatus.COMPLETED:
            raise exceptions.NoCompletedLessonError()

    @property
    def tutor(self):
        return self.lesson.tutor

    @property
    def student(self):
        return self.lesson.student
    
    def __str__(self):
        return f"Review from {self.lesson.student.username} -> {self.lesson.tutor.username}"
    
    class Meta:
        verbose_name="Review"
        verbose_name_plural="Reviews"

class Rating(BaseModel):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='rating')
    explanation = RatingField()
    communication = RatingField()
    materials = RatingField()
    organization = RatingField()
    individual_approach = RatingField()

    @property
    def average(self):
        return find_average(
            self.explanation, 
            self.communication,
            self.materials,
            self.organization,
            self.individual_approach
        )

    def __str__(self):
        return f"Rating for Review {self.review.id}"
    
    class Meta:
        verbose_name="Rating"
        verbose_name_plural="Ratings"
