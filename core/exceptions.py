from django.core.exceptions import ValidationError

class TutorRoleError(ValidationError):
    """Raised when the selected account is not a tutor."""
    def __init__(self):
        super().__init__({
            "tutor": "Selected account must have Tutor role."
        })


class StudentRoleError(ValidationError):
    """Raised when the selected account is not a student."""
    def __init__(self):
        super().__init__({
            "student": "Selected account must have Student role."
        })


class InvalidTimeRangeError(ValidationError):
    """Raised when the end time is earlier than the start time."""
    def __init__(self):
        super().__init__({
            "end_time": "End time must be later than start time."
        })

class NotTutorSubjectError(ValidationError):
    """Raised when choosen subject does not belong to choosen tutor"""
    def __init__(self):
        super().__init__({
                "subject": "The selected subject does not belong to this tutor."
        })

class NoCompletedLessonError(ValidationError):
    """Raised when student tries to create review to tutor they had no lesson with."""
    def __init__(self):
        super().__init__({
            "lesson": "Student has no completed lessons with this tutor."
        })

class PasswordsNotMatchError(ValidationError):
    """Raised when password and confirm password doesn't match."""
    def __init__(self):
        super().__init__({
            "password": "Password and confirm password doesn't match."
        })