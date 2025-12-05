from django.shortcuts import redirect

def user_logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if user is logged in via session
        if not request.session.get("user_name"):
            return redirect("coreapi:login_page")
        return view_func(request, *args, **kwargs)
    return wrapper
