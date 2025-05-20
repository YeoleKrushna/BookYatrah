from django.db import models
from django.contrib.auth.models import User
from users.models import Book

class ExchangeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ]

    requester = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    requested_book = models.ForeignKey(Book, related_name='received_requests', on_delete=models.CASCADE)
    offered_book = models.ForeignKey(Book, related_name='offered_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.username} → {self.requested_book.title} (offered: {self.offered_book.title})"
