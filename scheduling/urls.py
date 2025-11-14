from django.urls import path

from . import views

urlpatterns = [
    # Dashboards
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("faculty/dashboard/", views.faculty_dashboard, name="faculty_dashboard"),

    # Faculty slot management
    path("faculty/slots/", views.faculty_slots_list, name="faculty_slots_list"),
    path("faculty/slots/new/", views.faculty_slot_create, name="faculty_slot_create"),
    path("faculty/slots/<int:slot_id>/", views.faculty_slot_detail, name="faculty_slot_detail"),

    # Student booking
    path("student/faculties/", views.faculty_list_for_students, name="faculty_list"),
    path("student/faculty/<int:faculty_id>/slots/", views.faculty_public_slots, name="faculty_public_slots"),
    path("student/slots/<int:slot_id>/book/", views.book_slot, name="book_slot"),
    path("student/bookings/", views.student_bookings_list, name="student_bookings_list"),
    path("student/bookings/<int:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"),
]