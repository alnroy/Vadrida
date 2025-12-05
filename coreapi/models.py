from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserProfile(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    ph_no = models.CharField(max_length=15)
    role = models.CharField(max_length=20)
    password = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Hash password only if it's new or changed
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_name} ({self.role})"
