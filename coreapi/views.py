from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import check_password
from .models import UserProfile
import json
from django.shortcuts import render, redirect
from .decorators import user_logged_in
from django.middleware.csrf import get_token
from django_ratelimit.decorators import ratelimit


def login_page(request):
    if request.session.get("user_name"):
        return redirect("coreapi:dashboard")
    return render(request, "login.html")

@user_logged_in
def dashboard(request):
    if not request.session.get("user_name"):
        return redirect("login_page")
    
    return render(request, "dashboard.html")


@csrf_protect
@ratelimit(key="ip", rate="5/m", block=True)
def login_api(request):
    get_token(request) 
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    # Parse JSON properly
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as e:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return JsonResponse({"error": "Email and password required"}, status=400)

    # Verify user exists
    try:
        user = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "Invalid email or password"}, status=401)

    # Verify password
    if not check_password(password, user.password):
        return JsonResponse({"error": "Invalid email or password"}, status=401)

    # Save session
    request.session["user_id"] = user.id
    request.session["user_name"] = user.user_name
    request.session["email"] = user.email
    request.session["role"]=user.role
    request.session.set_expiry(60 * 60 * 12)  # 12 hours
    
    # Make sure session is saved
    request.session.modified = True

    return JsonResponse({
        "success": True,
        "message": "Login successful",
        "redirect": "/coreapi/dashboard/"
    }, status=200)


def logout_api(request):
    request.session.flush()
    return JsonResponse({"message": "Logged out successfully"})


from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    if not request.session.get("user_role") == "admin":
        return redirect("dashboard")  # redirect non-admins
    users = UserProfile.objects.all()
    return render(request, "dashboard/admin_dashboard.html", {"users": users})
