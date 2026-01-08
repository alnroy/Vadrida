# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.chat_history, name='chat_history'),
    path('upload/', views.upload_chat_file, name='chat_upload'),
]