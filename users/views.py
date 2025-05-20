from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from exchanges.models import ExchangeRequest
from .forms import (
    LoginForm,
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    BookUploadForm
)
from .models import Book

def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = user.profile
            if profile.phone and profile.city:
                return redirect('users:dashboard')
            else:
                return redirect('users:profile')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated.')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')

from django.db.models import Q

@login_required
def dashboard_view(request):
    user = request.user
    profile = user.profile

    u_form = UserUpdateForm(instance=user)
    p_form = ProfileUpdateForm(instance=profile)

    user_books = Book.objects.filter(owner=user).order_by('-uploaded_at')

    # Incoming exchange requests (pending) for user's books
    exchange_requests = ExchangeRequest.objects.filter(
        requested_book__owner=user,
        status='pending'
    ).select_related('requester', 'requested_book', 'offered_book').order_by('-timestamp')

    # Ongoing exchanges where user is requester or owner and status is pending or accepted
    ongoing_exchanges = ExchangeRequest.objects.filter(
        Q(requester=user) | Q(requested_book__owner=user),
        status__in=['pending', 'accepted']
    ).select_related('requester', 'requested_book', 'offered_book').order_by('-timestamp')

    context = {
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form,
        'user_books': user_books,
        'exchange_requests': exchange_requests,  # Incoming pending requests
        'ongoing_exchanges': ongoing_exchanges,  # All ongoing exchanges (pending + accepted)
    }

    return render(request, 'users/dashboard.html', context)



@login_required
def upload_book_view(request):
    if request.method == 'POST':
        book_form = BookUploadForm(request.POST, request.FILES)
        if book_form.is_valid():
            book = book_form.save(commit=False)  # Only once here
            book.owner = request.user
            profile = request.user.profile
            book.location = f"{profile.city}, {profile.pincode}"
            book.save()
            book_form.save_m2m()  # Only this is needed to save many-to-many fields
            messages.success(request, f'Book "{book.title}" uploaded successfully.')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        book_form = BookUploadForm()

    return render(request, 'users/upload_book.html', {'book_form': book_form})



# ✅ EDIT BOOK VIEW
@login_required
def edit_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect('users:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookUploadForm(instance=book)

    return render(request, 'users/edit_book.html', {
        'form': form,
        'book': book
    })


# ✅ DELETE BOOK VIEW
@login_required
def delete_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk, owner=request.user)

    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect('users:dashboard')

    return render(request, 'users/dashboard.html', {
        'book': book
    })

from django.contrib.auth.models import User

@login_required
def user_profile(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    books = Book.objects.filter(owner=user_obj).order_by('-uploaded_at')
    context = {
        'profile_user': user_obj,
        'books': books,
    }
    return render(request, 'users/public_profile.html', context)
