from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('get/', views.get_notifications, name='get'),
    path('read/<int:notification_id>/', views.mark_notification_read, name='read'),
    path('clear_all/', views.clear_all_notifications, name='clear_all'),
]
