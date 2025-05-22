from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Notification

# ✅ GET notifications
@login_required
def get_notifications(request):
    # First, get the latest 10 non-message notifications
    other_notifications = Notification.objects.filter(
        user=request.user
    ).exclude(notification_type='message_received').order_by('-created_at')

    # ✅ Now get latest message notifications but only 1 per sender (deduplicated)
    message_notifications = {}
    message_qs = Notification.objects.filter(
        user=request.user,
        notification_type='message_received'
    ).order_by('-created_at')

    for n in message_qs:
        # Use sender ID as unique key
        if n.sender_id not in message_notifications:
            message_notifications[n.sender_id] = n

    # Combine both sets
    combined = list(message_notifications.values()) + list(other_notifications[:10])
    combined.sort(key=lambda x: x.created_at, reverse=True)

    data = [
        {
            'id': n.id,
            'message': n.message,
            'url': n.url,
            'is_read': n.is_read
        } for n in combined[:10]  # limit to latest 10 in total
    ]
    return JsonResponse({'notifications': data})

# ✅ Mark single notification as read and redirect
@login_required
def mark_notification_read(request, notification_id):
    try:
        n = Notification.objects.get(id=notification_id, user=request.user)
        n.is_read = True
        n.save()
        return redirect(n.url)
    except Notification.DoesNotExist:
        return redirect('home:index')

# ✅ Clear all notifications
@require_POST
@login_required
def clear_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'success'})
