# exceptions/lessons.py
from django.core.exceptions import ValidationError

class LessonTimeConflictError(ValidationError):
    """Raised when the lesson overlaps with another lesson."""

    def __init__(self):
        super().__init__({
            "start_time": "The tutor already has another lesson during this time."
        })

class TutorNotAvailableError(ValidationError):
    """Raised when the lesson is outside the tutor's availability."""
    def __init__(self):
        super().__init__({
            "start_time": "The selected time is outside the tutor's availability."
        })

class LessonInPastError(ValidationError):
    """Raised when the lesson date is in the past."""
    def __init__(self):
        super().__init__({
            "date": "The selected date is in the past."
        })