from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from users.models import Book
from .models import ExchangeRequest
from notifications.models import Notification

# ✅ 1. Initiate Exchange - includes "exchange request sent" notification
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

        # ✅ Send notification to the book owner
        Notification.objects.create(
            user=book.owner,
            sender=request.user,
            notification_type='exchange_sent',
            message=f"{request.user.username} sent you an exchange request for '{book.title}'.",
            url=reverse('users:dashboard')
        )

        return redirect('exchanges:exchange_sent', book_id=book.id)

    return render(request, 'exchanges/select_offer_book.html', {
        'book': book,
        'user_books': user_books,
    })


# ✅ 2. Show "Exchange Sent" Page
@login_required
def exchange_sent(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'exchanges/exchange_sent.html', {'book': book})


# ✅ 3. Accept Exchange Request - includes "exchange accepted" notification
@login_required
def accept_request(request, request_id):
    try:
        exchange_request = ExchangeRequest.objects.get(id=request_id)
    except ExchangeRequest.DoesNotExist:
        messages.error(request, "Exchange request does not exist.")
        return redirect('users:dashboard')

    if exchange_request.status != 'pending':
        messages.info(request, "This exchange request has already been processed.")
        return redirect('users:dashboard')

    if exchange_request.requested_book.owner != request.user:
        return HttpResponseForbidden("You cannot accept this request.")

    if request.method == 'POST':
        exchange_request.status = 'accepted'
        exchange_request.save()
        messages.success(request, f"Exchange request accepted.")

        # Notification
        Notification.objects.create(
            user=exchange_request.requester,
            sender=request.user,
            notification_type='exchange_accepted',
            message=f"{request.user.username} accepted your exchange request.",
            url=reverse('chat:chat_room', args=[exchange_request.id])
        )

        return redirect(reverse('chat:chat_room', args=[exchange_request.id]))

    return redirect('users:dashboard')



# ✅ 4. Decline Exchange Request - includes "exchange declined" notification
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

        # ✅ Send notification to requester
        Notification.objects.create(
            user=exchange_request.requester,
            sender=request.user,
            notification_type='exchange_declined',
            message=f"{request.user.username} declined your exchange request for '{exchange_request.requested_book.title}'.",
            url=reverse('users:dashboard')
        )

        return redirect('users:dashboard')

    return redirect('users:dashboard')
