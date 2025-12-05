from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [
        '/coreapi/login/',
        '/coreapi/login/api/',
        '/',
        '/services/',
        '/contact/',
        '/about/',
        '/work/',
        ]

        # Allow static/media
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Skip API endpoints that expect JSON
        if request.path.startswith('/coreapi/login/api/'):
            return self.get_response(request)

        user_authenticated = request.session.get("user_id") is not None
        if not user_authenticated and request.path not in allowed_paths:
            return redirect('/coreapi/login/')

        return self.get_response(request)
