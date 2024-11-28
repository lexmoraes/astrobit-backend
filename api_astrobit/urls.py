from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),
]
