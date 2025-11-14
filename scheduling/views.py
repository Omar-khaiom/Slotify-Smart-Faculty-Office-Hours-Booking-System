from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.db import transaction
from django.contrib import messages

from .models import Slot, Booking
from accounts.models import User
from .forms import SlotCreateForm


@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You are not a student.")
    upcoming = Booking.objects.filter(student=request.user, status=Booking.Status.BOOKED, slot__start_time__gte=timezone.now()).order_by("slot__start_time")[:10]
    return render(request, "scheduling/student_dashboard.html", {"upcoming_bookings": upcoming})


@login_required
def faculty_dashboard(request):
    if not request.user.is_faculty():
        return HttpResponseForbidden("You are not a faculty member.")
    next_slots = Slot.objects.filter(faculty=request.user, start_time__gte=timezone.now()).order_by("start_time")[:10]
    return render(request, "scheduling/faculty_dashboard.html", {"next_slots": next_slots})


@login_required
def faculty_slots_list(request):
    if not request.user.is_faculty():
        return HttpResponseForbidden("Not faculty")
    slots = Slot.objects.filter(faculty=request.user).order_by("-start_time")
    return render(request, "scheduling/faculty_slots_list.html", {"slots": slots})


@login_required
def faculty_slot_detail(request, slot_id: int):
    if not request.user.is_faculty():
        return HttpResponseForbidden("Not faculty")
    slot = get_object_or_404(Slot, pk=slot_id, faculty=request.user)
    bookings = slot.bookings.select_related("student").order_by("created_at")
    return render(request, "scheduling/slot_detail.html", {"slot": slot, "bookings": bookings})


@login_required
def faculty_slot_create(request):
    if not request.user.is_faculty():
        return HttpResponseForbidden("Not faculty")
    if request.method == "POST":
        form = SlotCreateForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.faculty = request.user
            slot.save()
            messages.success(request, f"Slot created successfully for {slot.start_time.strftime('%b %d, %Y %I:%M %p')}")
            return redirect("faculty_slots_list")
    else:
        form = SlotCreateForm()
    return render(request, "scheduling/faculty_slot_create.html", {"form": form})


@login_required
def faculty_public_slots(request, faculty_id: int):
    if not request.user.is_student():
        return HttpResponseForbidden("Students only")
    faculty = get_object_or_404(User, pk=faculty_id, role=User.Role.FACULTY)
    slots = Slot.objects.filter(faculty=faculty, status=Slot.Status.AVAILABLE, start_time__gte=timezone.now()).order_by("start_time")
    return render(request, "scheduling/faculty_public_slots.html", {"faculty": faculty, "slots": slots})


@login_required
def faculty_list_for_students(request):
    """List all faculty members so a student can click rather than guessing IDs."""
    if not request.user.is_student():
        return HttpResponseForbidden("Students only")
    faculties = User.objects.filter(role=User.Role.FACULTY).order_by("username")
    return render(request, "scheduling/faculty_list.html", {"faculties": faculties})


@login_required
def book_slot(request, slot_id: int):
    if not request.user.is_student():
        return HttpResponseForbidden("Students only")
    slot = get_object_or_404(Slot, pk=slot_id, status=Slot.Status.AVAILABLE)
    # Capacity check & overlap prevention
    with transaction.atomic():
        current_count = Booking.objects.select_for_update().filter(slot=slot, status=Booking.Status.BOOKED).count()
        if current_count >= slot.max_students:
            messages.error(request, "This slot is already full.")
            return redirect("faculty_public_slots", faculty_id=slot.faculty.id)
        # Overlap: student has another booking that overlaps time range
        overlap = Booking.objects.filter(
            student=request.user,
            status=Booking.Status.BOOKED,
            slot__start_time__lt=slot.end_time,
            slot__end_time__gt=slot.start_time,
        ).exists()
        if overlap:
            messages.error(request, "You already have a booking that conflicts with this time slot.")
            return redirect("faculty_public_slots", faculty_id=slot.faculty.id)
        Booking.objects.create(slot=slot, student=request.user)
        messages.success(request, f"Successfully booked slot with {slot.faculty.username} on {slot.start_time.strftime('%b %d, %Y %I:%M %p')}")
    return redirect("student_bookings_list")


@login_required
def student_bookings_list(request):
    if not request.user.is_student():
        return HttpResponseForbidden("Students only")
    bookings = Booking.objects.filter(student=request.user).order_by("-created_at")
    return render(request, "scheduling/student_bookings_list.html", {"bookings": bookings})


@login_required
def cancel_booking(request, booking_id: int):
    if not request.user.is_student():
        return HttpResponseForbidden("Students only")
    booking = get_object_or_404(Booking, pk=booking_id, student=request.user, status=Booking.Status.BOOKED)
    booking.status = Booking.Status.CANCELLED
    booking.save(update_fields=["status"])
    messages.info(request, f"Booking with {booking.slot.faculty.username} on {booking.slot.start_time.strftime('%b %d, %I:%M %p')} has been cancelled.")
    return redirect("student_bookings_list")
