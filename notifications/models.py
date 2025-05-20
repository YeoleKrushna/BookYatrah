from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('exchange_accepted', 'Exchange Accepted'),
        ('exchange_declined', 'Exchange Declined'),
        ('message_received', 'Message Received'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # recipient
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    url = models.URLField()  # where the user should go when clicked
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username} - {self.notification_type}"
