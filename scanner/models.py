from django.db import models


class Attendee(models.Model):
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique registration number encoded in QR"
    )

    name = models.CharField(
        max_length=100,
        help_text="Attendee full name"
    )

    attended = models.BooleanField(
        default=False,
        help_text="Attendance status"
    )

    checked_in_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Time when attendance was marked"
    )

    

    class Meta:
        ordering = ["registration_number"]


    def __str__(self):
        return f"{self.registration_number} - {self.name}"
