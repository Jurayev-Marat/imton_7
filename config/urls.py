# config/urls.py (asosiy urls.py)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin paneli
    path('', include('configapp.urls')),  # Sizning ilovangiz
]