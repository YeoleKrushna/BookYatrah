from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from users.models import Book
from .models import ExchangeRequest

@login_required
def initiate_exchange(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Prevent offering on own book
    if book.owner == request.user:
        return redirect('home:index')

    user_books = Book.objects.filter(owner=request.user)

    if request.method == 'POST':
        offered_book_id = request.POST.get('offered_book_id')
        offered_book = get_object_or_404(Book, id=offered_book_id, owner=request.user)

        # Avoid duplicate requests
        if ExchangeRequest.objects.filter(requester=request.user, requested_book=book, offered_book=offered_book).exists():
            return redirect('exchanges:exchange_sent', book_id=book.id)

        exchange_request = ExchangeRequest.objects.create(
            requester=request.user,
            requested_book=book,
            offered_book=offered_book,
        )
        return redirect('exchanges:exchange_sent', book_id=book.id)

    return render(request, 'exchanges/select_offer_book.html', {
        'book': book,
        'user_books': user_books,
    })


@login_required
def exchange_sent(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'exchanges/exchange_sent.html', {'book': book})

from django.contrib import messages
from django.http import HttpResponseForbidden

@login_required
def accept_request(request, request_id):
    exchange_request = get_object_or_404(ExchangeRequest, id=request_id, status='pending')

    # Only the owner of the requested book can accept
    if exchange_request.requested_book.owner != request.user:
        return HttpResponseForbidden("You cannot accept this request.")

    if request.method == 'POST':
        exchange_request.status = 'accepted'
        exchange_request.save()
        messages.success(request, f"Exchange request accepted.")
        return redirect('users:dashboard')

    # Optionally: render a confirmation page before accept
    return redirect('users:dashboard')

@login_required
def decline_request(request, request_id):
    exchange_request = get_object_or_404(ExchangeRequest, id=request_id, status='pending')

    # Only the owner of the requested book can decline
    if exchange_request.requested_book.owner != request.user:
        return HttpResponseForbidden("You cannot decline this request.")

    if request.method == 'POST':
        exchange_request.status = 'declined'
        exchange_request.save()
        messages.info(request, f"Exchange request declined.")
        return redirect('users:dashboard')

    return redirect('users:dashboard')
