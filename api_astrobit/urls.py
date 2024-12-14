from django.urls import path
from rest_framework.routers import DefaultRouter

from api_astrobit import viewset, views

router = DefaultRouter()
router.register('users', viewset.CustomUserViewSet)
router.register('game_cards', viewset.GameCardDataViewSet)
urlpatterns = router.urls

urlpatterns = [

    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoints da API para login, registro e logout
    path('register/', views.RegisterUserView.as_view(), name='register'),  # Registro de usuário via API
    path('login/', views.LoginUserView.as_view(), name='login'),  # Login de usuário via API
    path('logout/', views.LogoutUserView.as_view(), name='logout'),  # Logout via API
    path('reset/', views.PasswordResetRequestView.as_view(), name='reset_password_request'),
    # Solicita reset de senha via API
    path('confirmreset/', views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    # Confirma reset de senha via API
    path('users/', views.CustomUserUpdateAPIView.as_view(), name='user_update')

]

urlpatterns += router.urls
