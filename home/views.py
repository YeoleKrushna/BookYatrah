from django.shortcuts import render, get_object_or_404
from users.models import Book, Profile
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def index(request):
    trending_books = Book.objects.all().order_by('-uploaded_at')[:6]
    latest_books = Book.objects.all().order_by('-uploaded_at')[:6]

    genre_books = []
    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
            preferred_genres = user_profile.preferred_genres.all()
            if preferred_genres.exists():
                genre_books = Book.objects.filter(
                    genres__in=preferred_genres
                ).distinct().exclude(owner=request.user)[:6]
        except Profile.DoesNotExist:
            pass

    context = {
        'trending_books': trending_books,
        'genre_books': genre_books,
        'latest_books': latest_books,
    }
    return render(request, 'home/index.html', context)


# ✅ Book detail view
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'home/book_detail.html', {'book': book})

def more_books(request):
    book_type = request.GET.get('type', 'all')

    if book_type == 'latest':
        books = Book.objects.order_by('-uploaded_at')[:10]
        heading = "Latest Uploaded Books"
    elif book_type == 'preferred' and request.user.is_authenticated:
        preferred_genres = request.user.profile.preferred_genres.all()
        books = Book.objects.filter(genres__in=preferred_genres).distinct()
        heading = "Books Based on Your Preferred Genres"
    else:
        books = Book.objects.all()
        heading = "All Books"

    return render(request, 'home/more_books.html', {
        'books': books,
        'heading': heading,
    })