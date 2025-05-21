# home/urls.py
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'), 
    path('more-books/', views.more_books, name='more_books'),
    path('search/', views.search, name='search'),

]
