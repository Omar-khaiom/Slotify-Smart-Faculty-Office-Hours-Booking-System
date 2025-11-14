from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        FACULTY = "FACULTY", "Faculty"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    department = models.CharField(max_length=100, blank=True)

    def is_student(self) -> bool:
        return self.role == self.Role.STUDENT

    def is_faculty(self) -> bool:
        return self.role == self.Role.FACULTY

    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN
