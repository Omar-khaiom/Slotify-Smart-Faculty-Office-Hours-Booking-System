from django.contrib import admin

from .models import Slot, Booking


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("faculty", "start_time", "end_time", "status", "max_students")
    list_filter = ("status", "faculty")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("student", "slot", "status", "created_at")
    list_filter = ("status",)
