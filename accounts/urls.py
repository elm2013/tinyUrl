from django.urls import path
from .views import RegisterView,UserRetrieveUpdateAPIView


urlpatterns = [
    
    path('v1/register/', RegisterView.as_view(), name="sign_up"),
    path('v1/update/', UserRetrieveUpdateAPIView.as_view(), name='user_retrieve'),
]
  