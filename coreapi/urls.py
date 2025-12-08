from django.urls import path
from . import views

app_name = "coreapi"

urlpatterns = [
    # Authentication APIs
    path("login/api/", views.login_api, name="login_api"),
    path("logout/api/", views.logout_api, name="logout_api"),

    # Folder/File APIs
    path("api/folders/", views.get_folders_api, name="get_folders_api"),          # updated name
    path("api/files-in-folder/", views.get_files_in_folder_api, name="get_files_in_folder_api"),  # new endpoint
    path('api/file-info/', views.get_file_info, name='get_file_info'),
    path('api/analyze/', views.analyze_file, name='analyze_file'),

    # File serving
    path('serve-file/', views.serve_file, name='serve_file'),

    # Pages
    path("login/", views.login_page, name="login_page"),
    path("manager/", views.admin_dashboard, name="admin_dashboard"),
    path("office/", views.office_dashboard, name="office_dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
