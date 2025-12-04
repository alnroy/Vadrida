from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserProfile(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    ph_no = models.CharField(max_length=15)
    role = models.CharField(max_length=20)
    password = models.CharField(max_length=200,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.user_name} ({self.role})"
