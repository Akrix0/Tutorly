# exceptions/profiles.py
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

class TimeIntervalsOverlapError(ValidationError):
    """Raised when two time intervals overlap."""
    def __init__(self):
        super().__init__({
            "start_time": "Time intervals overlap."
        })

class TooYoungError(ValidationError):
    """Raised when tutor is 14 years old or younger."""
    def __init__(self):
        super().__init__({
            "birth_date": "You are too young to be a tutor."
        })

class InvalidDataError(ValidationError):
    """Raised when provided data is invalid."""
    def __init__(self, data=None):
        if data:
            super().__init__({
                data: f"Invalid {data} provided."
            })
        else:
            super().__init__({
                "data": "Invalid data provided."
            })

class DuplicateSubjectsError(ValidationError):
    """Raised when same two subjects were provided."""
    def __init__(self):
        super().__init__({
            "subject": "Two same subjects were provided."
        })


class NotTutorSubjectError(ValidationError):
    """Raised when selected subject does not belong to selected tutor."""
    def __init__(self):
        super().__init__({
                "subject": "The selected subject does not belong to this tutor."
        })


class TutorSubjectExistsError(ValidationError):
    """Raised when selected subject already exists for this tutor."""
    def __init__(self):
        super().__init__({
                "subject": "The selected subject already exists for this tutor."
        })