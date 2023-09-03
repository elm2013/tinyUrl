from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
import shortuuid
from .models import URL
from .serializers import URLSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_short_url(request):
    user = request.user
    original_url = request.data.get('url') 
  

    if not original_url:
        return Response({'error': 'URL field is required'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)  
   
    if not URL.objects.filter(original_url=original_url,expiration_date__gte=timezone.now()).exists():
        short_url = URL.objects.create(original_url=original_url)
        short_url.user.add(user)
    else:
        short_url =  URL.objects.get(original_url=original_url)
       
    
    serializer = URLSerializer(short_url)
 
    return Response(serializer.data, status=status.HTTP_201_CREATED)
   


@api_view(['GET'])
def get_short_url(request, tiny_url):
    short_url = get_object_or_404(URL, tiny_url=tiny_url)

    if short_url.is_expired():
        return Response({'error': 'URL has expired'}, status=status.HTTP_404_NOT_FOUND)

    serializer = URLSerializer(short_url)
    return redirect((serializer.data['original_url']))
 


@api_view(['GET'])
def list_short_urls(request):
    paginator = PageNumberPagination()
    size = request.GET.get("limit", 1)
    paginator.page_size = size  # تعداد آیتم‌ها در هر صفحه
    queryset = URL.objects.all()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = URLSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

    
    