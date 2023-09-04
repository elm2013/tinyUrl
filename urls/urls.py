from django.urls import path

from .views import createShortUrl, getShortUrl, getListShortUrlpagging,getMyListShortUrlpagging

urlpatterns = [
    path('v1/submiturl/', createShortUrl.as_view(), name='create short url'),
    path('v1/gettiny/<str:tiny_url>/', getShortUrl.as_view(), name='get short url'),
    path('v1/getall/', getListShortUrlpagging.as_view(), name='list short urls'),
    path('v1/getMyUrl/', getMyListShortUrlpagging.as_view(), name='My list short urls'),
]