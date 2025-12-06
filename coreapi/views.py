from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import check_password
from .models import UserProfile
import json
from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from django_ratelimit.decorators import ratelimit


def login_page(request):
    if request.session.get("user_id"):
        return redirect("coreapi:dashboard")
    return render(request, "login.html")

def admin_dashboard(request):
    users = UserProfile.objects.all()
    return render(request, "admin_dashboard.html", {"users": users})

def office_dashboard(request):
    return render(request, "office_dashboard.html")


def dashboard(request):
    role = request.session.get("user_role")

    # Role-based redirect
    if role == "admin":
        return redirect("coreapi:admin_dashboard")

    if role == "office":
        return redirect("coreapi:office_dashboard")
    
    if role == "IT":
        return redirect("coreapi:office_dashboard")
    
    return JsonResponse({"error": "Invalid"}, status=401)
    

@csrf_protect
@ratelimit(key="ip", rate="5/m", block=True)
def login_api(request):
    get_token(request)

    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    # Parse JSON
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return JsonResponse({"error": "Email and password required"}, status=400)
    # Check user
    try:
        user = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "Invalid email or password"}, status=401)

    # Check password
    if not check_password(password, user.password):
        return JsonResponse({"error": "Invalid email or password"}, status=401)

    # SESSION SAVE
    request.session["user_id"] = user.id
    request.session["user_name"] = user.user_name
    request.session["user_email"] = user.email
    request.session["user_role"] = user.role   

    request.session.set_expiry(60 * 60 * 12)  # 12 hours
    request.session.modified = True

    # API Response
    return JsonResponse({
        "success": True,
        "message": "Login successful",
        "redirect": "/coreapi/dashboard/"
    }, status=200)


def logout_api(request):
    request.session.flush()
    return JsonResponse({"message": "Logged out successfully"})
