from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from .models import ChatMessage
from exchanges.models import ExchangeRequest
from notifications.models import Notification


@login_required
def inbox(request):
    exchanges = ExchangeRequest.objects.filter(
        status='accepted'
    ).filter(
        Q(requester=request.user) | Q(requested_book__owner=request.user)
    )
    return render(request, 'chat/inbox.html', {'exchanges': exchanges})


@login_required
def chat_room(request, exchange_id):
    exchange = get_object_or_404(ExchangeRequest, id=exchange_id)

    # Block access if exchange is not accepted
    if exchange.status != 'accepted':
        messages.error(request, "This chat has been closed or cancelled.")
        return redirect('chat:inbox')

    # Only participants can access
    if request.user != exchange.requester and request.user != exchange.requested_book.owner:
        return redirect('home:index')

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(
                exchange=exchange,
                sender=request.user,
                message=message
            )

            # Notify recipient
            recipient = exchange.requester if request.user != exchange.requester else exchange.requested_book.owner

            Notification.objects.create(
                user=recipient,
                sender=request.user,
                notification_type='message_received',
                message=f"New message from {request.user.username}",
                url=reverse('chat:chat_room', args=[exchange.id])
            )

        return redirect('chat:chat_room', exchange_id=exchange.id)

    messages_qs = ChatMessage.objects.filter(exchange=exchange).order_by('timestamp')
    return render(request, 'chat/chat_room.html', {
        'exchange': exchange,
        'messages': messages_qs
    })


@login_required
def delete_chat(request, exchange_id):
    exchange = get_object_or_404(ExchangeRequest, id=exchange_id)

    # Only requester or requested book owner can delete
    if request.user != exchange.requester and request.user != exchange.requested_book.owner:
        return redirect('home:index')

    if request.method == 'POST':
        # Identify the other participant (recipient of cancellation notification)
        recipient = exchange.requester if request.user != exchange.requester else exchange.requested_book.owner

        # Delete all chat messages related to this exchange (if CASCADE not enabled)
        ChatMessage.objects.filter(exchange=exchange).delete()

        # Delete the exchange itself
        exchange.delete()

        # Send notification about cancellation
        Notification.objects.create(
            user=recipient,
            sender=request.user,
            notification_type='exchange_cancelled',
            message=f"{request.user.username} cancelled the exchange.",
            url=reverse('chat:inbox')
        )

        messages.warning(request, "Exchange and related chat deleted. The other user has been notified.")
        return redirect('chat:inbox')

    # If GET request, redirect to inbox
    return redirect('chat:inbox')
