from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Slot(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        BLOCKED = "BLOCKED", "Blocked"
        CANCELLED = "CANCELLED", "Cancelled"
        PAST = "PAST", "Past"

    faculty = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="slots",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    max_students = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.faculty} | {self.start_time} - {self.end_time}"

    @property
    def booked_count(self) -> int:
        """Number of active bookings (excludes cancelled/no-show/completed)."""
        return self.bookings.filter(status=Booking.Status.BOOKED).count()


class Booking(models.Model):
    class Status(models.TextChoices):
        BOOKED = "BOOKED", "Booked"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"
        NO_SHOW = "NO_SHOW", "No Show"

    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BOOKED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} -> {self.slot}"
