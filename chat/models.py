from django.db import models
from django.contrib.auth.models import User
from exchanges.models import ExchangeRequest

class ChatMessage(models.Model):
    exchange = models.ForeignKey(ExchangeRequest, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} ({self.timestamp}): {self.message}"
