from django.urls import path
from . import views

app_name = 'exchanges'

urlpatterns = [
    path('initiate/<int:book_id>/', views.initiate_exchange, name='initiate_exchange'),
    path('sent/<int:book_id>/', views.exchange_sent, name='exchange_sent'),
]

urlpatterns += [
    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('decline/<int:request_id>/', views.decline_request, name='decline_request'),
]
