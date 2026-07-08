from django.db import models
from django.core.validators import MinValueValidator

from django_countries.fields import CountryField

from accounts.models import Account
from core import exceptions, utils
from core.models import BaseModel, Currency

class TutorCard(BaseModel):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="tutor_card",
    )

    birth_date = models.DateField()
    experience_years = models.PositiveSmallIntegerField()
    country = CountryField()

    @property
    def age(self):
        return utils.get_age(self.birth_date)

    def clean(self):
        super().clean()

        if self.account.role != Account.UserRole.TUTOR:
            raise exceptions.TutorRoleError()
        
        if self.experience_years >= self.age - 12:
            raise exceptions.InvalidDataError("experience_years")
        
        if utils.get_age(self.age) <= 14:
            raise exceptions.TooYoungError()

    def __str__(self):
        return f"TutorCard for {self.account.username} ({self.country.name})"

    class Meta:
        verbose_name = "Tutor Card"
        verbose_name_plural = "Tutor Cards"

class Subject(BaseModel):
    class SubjectNames(models.TextChoices):
        # Languages & Literature
        ENGLISH_LANG = "english_lang", "English Language"
        ENGLISH_LITR = "english_litr", "English Literature"

        FRENCH_LANG = "french_lang", "French Language"
        FRENCH_LITR = "french_litr", "French Literature"

        GERMAN_LANG = "german_lang", "German Language"
        GERMAN_LITR = "german_litr", "German Literature"

        SPANISH_LANG = "spanish_lang", "Spanish Language"
        SPANISH_LITR = "spanish_litr", "Spanish Literature"

        UKRAINIAN_LANG = "ukrainian_lang", "Ukrainian Language"
        UKRAINIAN_LITR = "ukrainian_litr", "Ukrainian Literature"

        # Other subjects
        MATH = "math", "Math"
        PHYSICS = "physics", "Physics"
        GEOGRAPHY = "geography", "Geography"
        CHEMISTRY = "chemistry", "Chemistry"
        BIOLOGY = "biology", "Biology"
        HISTORY = "history", "History"

    name = models.CharField(max_length=64, choices=SubjectNames.choices, unique=True, editable=False)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

class Availability(BaseModel):
    class WeekDay(models.IntegerChoices):
        MONDAY = 1, "Monday"
        TUESDAY = 2, "Tuesday"
        WEDNESDAY = 3, "Wednesday"
        THURSDAY = 4, "Thursday"
        FRIDAY = 5, "Friday"
        SATURDAY = 6, "Saturday"
        SUNDAY = 7, "Sunday"
    tutor_card = models.ForeignKey(
        TutorCard,
        on_delete=models.CASCADE,
        related_name="availability",
    )
    weekday = models.PositiveSmallIntegerField(
        choices=WeekDay.choices
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        super().clean()

        if self.start_time >= self.end_time:
            raise exceptions.InvalidTimeRangeError()

    def __str__(self):
        return f"{self.get_weekday_display()} {self.start_time} - {self.end_time} for {self.tutor_card.account.username}"

    class Meta:
        verbose_name = "Availability"
        verbose_name_plural = "Availabilities"

class TutorSubject(BaseModel):
    tutor_card = models.ForeignKey(TutorCard, on_delete=models.CASCADE, related_name="subjects")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="tutor_subjects")
    price_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(1)
        ]
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )

    def __str__(self):
        return f"{self.subject.get_name_display()} for {self.tutor_card.account.username} at ${self.price_per_hour}/hour"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tutor_card", "subject"],
                name="unique_tutor_subject",
            )
        ]
        ordering = ["subject__name"]
        verbose_name = "Tutor Subject"
        verbose_name_plural = "Tutor Subjects"