from django.urls import path
from .views import SignUpAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('api/singup/', SignUpAPIView.as_view(), name='api-signup'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/homepage/', LoginAPIView.as_view(), name='homepage'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
]