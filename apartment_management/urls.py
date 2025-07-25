from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),  # Include core URLs first
    path('admin/', admin.site.urls),  # Admin URLs after core URLs
]