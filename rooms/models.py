from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    topic = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="rooms")

   

    class Meta:
        unique_together = ["topic", "created_by"]


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    

    class Meta:
        ordering = ["-created_at"]
