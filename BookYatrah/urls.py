from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('users/', include('users.urls')),
    path('exchanges/', include('exchanges.urls')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('notifications/', include('notifications.urls')),
]

# Always serve media files via Django (only recommended in development or when you want Django to serve media)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
