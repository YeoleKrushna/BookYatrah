from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('room/<int:exchange_id>/', views.chat_room, name='chat_room'),
    path('inbox/', views.inbox, name='inbox'),
    path('delete/<int:exchange_id>/', views.delete_chat, name='delete_chat'),
]
