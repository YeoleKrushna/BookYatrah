from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from exchanges.models import ExchangeRequest
from django.db.models import Q

@login_required
def chat_room(request, exchange_id):
    exchange = get_object_or_404(ExchangeRequest, id=exchange_id, status='accepted')

    # Only participants can access the chat room
    if request.user != exchange.requester and request.user != exchange.requested_book.owner:
        return redirect('home:index')

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(
                exchange=exchange,
                sender=request.user,
                message=message  # Correct field name here
            )
        return redirect('chat:chat_room', exchange_id=exchange.id)

    messages = ChatMessage.objects.filter(exchange=exchange).order_by('timestamp')
    return render(request, 'chat/chat_room.html', {
        'exchange': exchange,
        'messages': messages
    })

@login_required
def inbox(request):
    exchanges = ExchangeRequest.objects.filter(
        status='accepted'
    ).filter(
        Q(requester=request.user) | Q(requested_book__owner=request.user)
    )
    return render(request, 'chat/inbox.html', {'exchanges': exchanges})
