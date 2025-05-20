from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    preferred_genres = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Book(models.Model):
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Good', 'Good'),
        ('Okay', 'Okay'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre, blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='book_images/')
    location = models.CharField(max_length=255)  # autofill from user profile
    preferred_genres = models.ManyToManyField(Genre, related_name='preferred_books', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
