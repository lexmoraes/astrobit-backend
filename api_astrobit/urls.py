from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_astrobit.views import (
    CustomTokenObtainPairView,
    RegisterUserView,
    LoginUserView,
    LogoutUserView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)
from api_astrobit.viewset import CustomUserViewSet, GameCardDataViewSet, RankUserViewSet

# Configurando o roteador do DRF
router = DefaultRouter()
router.register(
    r'users',
    CustomUserViewSet,
    basename='user'
)

router.register(
    r'game-cards',
    GameCardDataViewSet,
    basename='gamecard'
)

router.register(
    r'rank-users',
    RankUserViewSet,
    basename='rankuser'
)

router.register(
    r'register-users',
    RegisterUserView,
    basename='registeruser'
)

urlpatterns = [
    # Rotas gerenciadas pelo router
    path('api/',
         include(router.urls)),

    # Endpoints customizados
    path('api/token/',
         CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('api/register/',
         RegisterUserView.as_view(),
         name='signup'),

    path('api/login/',
         LoginUserView.as_view(),
         name='login'),

    path('api/logout/',
         LogoutUserView.as_view(),
         name='logout'),

    # Reset de senha
    path('api/password-reset/',
         PasswordResetRequestView.as_view(),
         name='password_reset'),

    path('api/password-reset-confirm/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'
    ),
]
