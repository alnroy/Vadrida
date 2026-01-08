import os

# 1️⃣ Configure settings FIRST
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vadrida.settings")

# 2️⃣ Load Django apps
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack      # <--- REQUIRED
from channels.sessions import SessionMiddlewareStack # <--- REQUIRED
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

# Initialize Django ASGI application early to ensure the AppRegistry is populated
# before importing code that may import ORM models.
django_asgi_app = ASGIStaticFilesHandler(get_asgi_application())

# 3️⃣ Import routing ONLY AFTER apps are ready
import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    
    # 4️⃣ Wrap WebSocket in Session & Auth Middleware
    "websocket": SessionMiddlewareStack(  # <--- Allows accessing request.session
        AuthMiddlewareStack(              # <--- Allows accessing request.user
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})