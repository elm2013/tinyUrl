from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes,throttle_classes
from rest_framework.response import Response
import shortuuid
from .models import URL
from .serializers import URLSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView



class createShortUrl(APIView):
    permission_classes = (IsAuthenticated,)
    createShortUrlSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'url': openapi.Schema(type=openapi.TYPE_STRING, description='string')        
    },
    required=['url']
)
    @swagger_auto_schema(request_body=createShortUrlSchema,operation_description="create a short url")
    def post(self, request, *args, **kwargs):
        user = request.user
        originalUrl = request.data.get('url')
        if not originalUrl:
            return Response({'error': 'URL field is required'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)  
    
        if not URL.objects.filter(original_url=originalUrl,expiration_date__gte=timezone.now()).exists():
            short_url = URL.objects.create(original_url=originalUrl)
            short_url.user.add(user)
        else:
            short_url =  URL.objects.get(original_url=originalUrl)
        
        
        serializer = URLSerializer(short_url)
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
class getShortUrl(APIView):
    throttle_classes = [AnonRateThrottle]
    @method_decorator(cache_page(60*60*2)) 
    @swagger_auto_schema(operation_description="redirect short url")   
  
    def get(request, tiny_url):
        short_url = get_object_or_404(URL, tiny_url=tiny_url)

        if short_url.is_expired():
            return Response({'error': 'URL has expired'}, status=status.HTTP_404_NOT_FOUND)

        serializer = URLSerializer(short_url)
        return redirect((serializer.data['original_url']))
 
class getListShortUrlpagging(APIView):
    permission_classes = (IsAuthenticated,)
    @method_decorator(cache_page(60*60*2)) 
    @swagger_auto_schema(operation_description="get all short url")   
    def get(self,request,**kwargs):
        paginator = PageNumberPagination()
        size = request.GET.get("limit", 1)
        paginator.page_size = size  # تعداد آیتم‌ها در هر صفحه
        queryset = URL.objects.all()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = URLSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class getMyListShortUrlpagging(APIView):
    permission_classes = (IsAuthenticated,)
    @method_decorator(cache_page(60*15)) 
    @method_decorator(vary_on_headers("Authorization",))
    @swagger_auto_schema(operation_description="get my short url")   
    def get(self,request,**kwargs):
        paginator = PageNumberPagination()
        size = request.GET.get("limit", 1)
        paginator.page_size = size  # تعداد آیتم‌ها در هر صفحه
        queryset = URL.objects.filter(user=request.user)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = URLSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    
    