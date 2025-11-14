from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_faculty():
                return redirect("faculty_dashboard")
            if user.is_student():
                return redirect("student_dashboard")
            return redirect("admin:index")
        return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """Custom logout to avoid method issues and show a friendly message."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")
