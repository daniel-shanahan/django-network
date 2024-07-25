from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField(
        "self", symmetrical=False, blank=True, null=True, related_name="followers"
    )


class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    liked_by = models.ManyToManyField(
        "User", blank=True, null=True, related_name="likes"
    )
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster.username}: {self.body}"

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "body": self.body,
            "liked": [user.username for user in self.liked_by.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
