from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    goal = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    def __str__(self):
        return self.goal


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    message = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{{self.user.username}} - {{self.message}}"
