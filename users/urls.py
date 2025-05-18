from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('upload-book/', views.upload_book_view, name='upload_book'),
    # New dashboard route - main user dashboard with tabs & book upload
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('book/<int:pk>/edit/', views.edit_book_view, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book_view, name='delete_book'),

]
