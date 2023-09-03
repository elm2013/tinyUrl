from django.urls import path

from .views import create_short_url, get_short_url, list_short_urls

urlpatterns = [
    path('api/create/', create_short_url, name='create_short_url'),
    path('api/get-tiny/<str:tiny_url>/', get_short_url, name='get_short_url'),
    path('api/get-all', list_short_urls, name='list_short_urls'),
]