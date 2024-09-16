from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request, "core/home.html")


# This decorator ensures that only authenticated users can access the dashboard
@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate the user using Django's built-in authenticate method
        # If credentials are correct ,authenticate() returns the 'user' Object
        # If they're incorrect ,authenticate() returns 'None'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If user is authenticated ,log them in(by creating a session)and redirect to the dashboard
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "core/login.html")


def logout_view(request):
    # This logs out the user by clearing their session
    logout(request)
    # After logout the user is redirect to the home page
    return redirect("home")
