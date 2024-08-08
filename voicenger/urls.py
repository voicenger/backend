from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from voicengerapp.urls import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('voicengerapp.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)