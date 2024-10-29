from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)