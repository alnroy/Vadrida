from django.urls import path
from . import views

app_name = "coreapi"

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("login/api/", views.login_api, name="login_api"),
    path("logout/api/", views.logout_api, name="logout_api"),

    # ADD THESE
    path("manager/", views.admin_dashboard, name="admin_dashboard"),
    path("office/", views.office_dashboard, name="office_dashboard"),

    path("dashboard/", views.dashboard, name="dashboard"),
]
