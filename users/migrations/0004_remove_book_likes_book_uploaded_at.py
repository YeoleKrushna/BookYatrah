# Generated by Django 5.2.1 on 2025-05-20 13:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_book_uploaded_at_book_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='likes',
        ),
        migrations.AddField(
            model_name='book',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
