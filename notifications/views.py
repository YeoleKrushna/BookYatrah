from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    data = [
        {
            'id': n.id,
            'message': n.message,
            'url': n.url,
            'is_read': n.is_read
        } for n in notifications
    ]
    return JsonResponse({'notifications': data})

@login_required
def mark_notification_read(request, notification_id):
    try:
        n = Notification.objects.get(id=notification_id, user=request.user)
        n.is_read = True
        n.save()
        return redirect(n.url)
    except Notification.DoesNotExist:
        return redirect('home:index')


# notifications/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Notification

@require_POST
@login_required
def clear_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'success'})
