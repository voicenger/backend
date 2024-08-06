from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("authentication.urls")),
    path('auth/', include('authentication.urls')),
    path('api/voicengerdb/', include('voicengerdb.urls')),
    path('api/chat/', include('chat.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Serves media files during development
