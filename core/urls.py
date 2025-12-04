from django.urls import path,include
from . import views

app_name = 'core'  # Important for namespacing

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('work/',views.work,name='work'),
    
]