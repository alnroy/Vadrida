import os

# 1️⃣ Configure settings FIRST
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vadrida.settings")

# 2️⃣ Load Django apps
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

django_asgi_app = ASGIStaticFilesHandler(get_asgi_application())

# 3️⃣ Import routing ONLY AFTER apps are ready
import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(chat.routing.websocket_urlpatterns),
})
