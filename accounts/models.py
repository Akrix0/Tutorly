from django.db import models
from django.contrib.auth.models import AbstractUser

from autoslug import AutoSlugField

from core.models import BaseModel
from core.utils import custom_slugify

class Account(AbstractUser, BaseModel):
    class UserRole(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Admin"
        STUDENT = "student", "Student"
        TUTOR = "tutor", "Tutor"
    
    username = models.CharField(max_length=128, unique=True)
    slug = AutoSlugField(populate_from="username", slugify=custom_slugify, unique=True, editable=False, auto_created=True)
    role = models.CharField(max_length=16, choices=UserRole.choices, default = UserRole.USER)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_student(self):
        return self.role == self.UserRole.STUDENT

    @property
    def is_tutor(self):
        return self.role == self.UserRole.TUTOR
    
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"