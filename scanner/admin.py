from django.contrib import admin
from .models import Attendee


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "name", "attended", "checked_in_at")
    search_fields = ("registration_number", "name")
    list_filter = ("attended",)
