from django.urls import path
from . import views

app_name = "coreapi"

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("login/submit/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout"),
]
