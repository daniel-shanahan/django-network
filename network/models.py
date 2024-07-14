from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster.username}: {self.body}"

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "body": self.body,
            "timestamp": self.timestamp.strf("%b %d %Y, %I:%M %p"),
        }
