from django.urls import path
from .views import chat_history, upload_chat_file, unpin_message

urlpatterns = [
    path("history/", chat_history),
    path("upload/", upload_chat_file),
    path("unpin/", unpin_message),
]
