from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserProfile
from django.contrib.auth.hashers import  check_password


def login_page(request):
    return render(request, "login.html")

def login_user(request):
    if request.method != "POST":
        return redirect("login.html")

    email = request.POST.get("email")
    user_id = request.POST.get("user_id")
    password=request.POST.get("passsword")
    try:
        user = UserProfile.objects.get(email=email, id=user_id)

        # Check hashed password
        if not check_password(password, user.password):
            messages.error(request, "Incorrect password")
            return redirect("login.html")

        # Save session
        request.session["user_id"] = user.id
        request.session["user_name"] = user.user_name
        request.session["user_role"] = user.role

        messages.success(request, "Login successful!")
        return redirect("dashboard.html")


    except UserProfile.DoesNotExist:
        messages.error(request, "Invalid email or user ID")
        return redirect("login.html")


def logout_user(request):
    logout(request)
    return redirect("login.html")
