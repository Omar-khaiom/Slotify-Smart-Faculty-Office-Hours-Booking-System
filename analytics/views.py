from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import ExtractHour
from scheduling.models import Booking, Slot
from accounts.models import User


@login_required
def analytics_dashboard(request):
    # Total bookings
    total_bookings = Booking.objects.filter(status=Booking.Status.BOOKED).count()
    total_slots = Slot.objects.count()
    
    # Peak hours (group by hour of day)
    peak_hours_data = (
        Booking.objects.filter(status=Booking.Status.BOOKED)
        .annotate(hour=ExtractHour('slot__start_time'))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    
    # Faculty with most bookings
    top_faculty = (
        User.objects.filter(role=User.Role.FACULTY)
        .annotate(booking_count=Count('slots__bookings', filter=Q(slots__bookings__status=Booking.Status.BOOKED)))
        .order_by('-booking_count')[:5]
    )
    
    # Recent activity
    recent_bookings = Booking.objects.select_related('student', 'slot__faculty').order_by('-created_at')[:10]
    
    context = {
        'total_bookings': total_bookings,
        'total_slots': total_slots,
        'peak_hours': peak_hours_data,
        'top_faculty': top_faculty,
        'recent_bookings': recent_bookings,
    }
    return render(request, "analytics/dashboard.html", context)
