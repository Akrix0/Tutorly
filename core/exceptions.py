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
    def __init__(self):
        super().__init__({
            "end_time": "End time must be later than start time."
        })