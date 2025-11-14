# Slotify – Smart Faculty Office Hours Booking System

A Django-based web application that simplifies scheduling and managing faculty office hours for educational institutions.

## Features

### For Students
- **Browse Faculty Directory**: View all available faculty members and their departments
- **Real-time Slot Booking**: See available office hour slots and book instantly
- **Booking Management**: View upcoming bookings, past appointments, and cancel when needed
- **Conflict Prevention**: System prevents double-booking and overlapping appointments

### For Faculty
- **Slot Creation**: Create one-time or recurring office hour slots
- **Booking Overview**: See who has booked each slot
- **Flexible Scheduling**: Set location (physical room or online), capacity limits, and time ranges
- **Dashboard**: Quick view of upcoming slots and recent bookings

### For Administrators
- **Analytics Dashboard**: 
  - Total bookings and slots created
  - Peak booking hours analysis
  - Most-booked faculty insights
  - Recent activity tracking
- **Django Admin Panel**: Full CRUD access to users, slots, and bookings

## Tech Stack

- **Backend**: Django 5.2+
- **Database**: SQLite (dev), MySQL/PostgreSQL-ready (production)
- **Frontend**: Bootstrap 5, Django Templates
- **Deployment Ready**: AWS EC2, RDS, S3, ALB, Auto Scaling

## Installation & Setup

### Prerequisites
- Python 3.10+
- pip
- Virtual environment tool (venv)

### Local Development

1. **Clone or navigate to project directory**
   ```powershell
   cd "d:\Slotify – Smart Faculty Office Hours Booking System"
   ```

2. **Create and activate virtual environment**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install django
   ```

4. **Apply migrations**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```powershell
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```powershell
   python manage.py runserver
   ```

7. **Access the application**
   - Homepage: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`
   - Login: `http://127.0.0.1:8000/login/`

## Usage Guide

### Setting Up Users

1. Log in to Django admin (`/admin/`)
2. Create faculty users:
   - Add user → set username, password
   - Set `role` to `FACULTY`
   - Optionally add `department`
3. Create student users:
   - Add user → set username, password
   - Set `role` to `STUDENT`

### Faculty Workflow

1. Login with faculty credentials
2. Navigate to **Dashboard** → **Create New Slot**
3. Fill in:
   - Start/End time (future datetime)
   - Location (room number or online link)
   - Max students (capacity)
4. View upcoming slots and bookings on dashboard

### Student Workflow

1. Login with student credentials
2. Navigate to **Browse Faculty**
3. Click **View Slots** for desired faculty
4. Click **Book** on available slot
5. View/manage bookings at **My Bookings**
6. Cancel if needed (redirects with confirmation message)

## Project Structure

```
slotify/
├── accounts/          # User management, auth, roles
├── scheduling/        # Slots, bookings, core logic
├── analytics/         # Reporting and insights
├── slotify/          # Project settings, URLs
├── templates/        # HTML templates
├── static/           # CSS, JS, images
├── db.sqlite3        # Local database
└── manage.py         # Django CLI
```

## Key Models

- **User**: Custom user with roles (STUDENT, FACULTY, ADMIN)
- **Slot**: Office hour time slots created by faculty
- **Booking**: Student bookings for specific slots

## Security & Validation

- Role-based access control (students can't create slots, faculty can't book)
- Booking capacity enforcement (prevents overbooking)
- Time conflict detection (prevents double-booking for students)
- CSRF protection on all forms
- Password hashing with Django's built-in validators

## Future Enhancements

- Email/SMS notifications for bookings and reminders
- Recurring slot templates (e.g., "every Monday 2-4pm")
- Calendar view integration
- Student reviews/ratings for office hours
- Export analytics to PDF/CSV
- React frontend for SPA experience
- AWS deployment with Auto Scaling, RDS, S3

## AWS Deployment (Planned)

- **EC2**: Django app with Gunicorn
- **RDS**: MySQL/PostgreSQL database
- **S3**: Static files and media storage
- **ALB**: Load balancing across instances
- **Auto Scaling**: Handle traffic spikes during exam periods
- **SES**: Email notifications

## License

Educational project for academic purposes.

## Contributors

Developed as part of a cloud computing and web development coursework.
