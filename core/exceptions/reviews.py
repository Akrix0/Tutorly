# exceptions/reviews.py
from django.core.exceptions import ValidationError

class NoCompletedLessonError(ValidationError):
    """Raised when student tries to create review to tutor they had no lesson with."""
    def __init__(self):
        super().__init__({
            "lesson": "Student has no completed lessons with this tutor."
        })