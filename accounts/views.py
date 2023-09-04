# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
# view for registering users
class RegisterView(APIView):
    @swagger_auto_schema(request_body=UserSerializer,operation_description="rigister user")
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserRetrieveUpdateAPIView(APIView):
    # Allow only authenticated users to access this url 
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    @swagger_auto_schema(operation_description="get info user")
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(request_body=UserSerializer,operation_description="get info user")
    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)