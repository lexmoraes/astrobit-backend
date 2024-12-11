from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_astrobit.views import CustomTokenObtainPairView, RegisterUserView, LoginUserView, LogoutUserView, \
    GameCardDataView, RankUserListView, CustomUserUpdateAPIView, PasswordResetRequestView, PasswordResetConfirmView
from api_astrobit.viewset import CustomUserViewSet, GameCardDataViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'game-cards', GameCardDataViewSet, basename='gamecarddata')

urlpatterns = [
    # URLs de API com o roteador
    path('api/', include(router.urls)),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoints da API para login, registro e logout
    path('api/register/', RegisterUserView.as_view(), name='user-register'),  # Registro de usuário via API
    path('api/login/', LoginUserView.as_view(), name='login-user'),  # Login de usuário via API
    path('api/logout/', LogoutUserView.as_view(), name='logout-user'),  # Logout via API
    path('api/reset/', PasswordResetRequestView.as_view(), name='reset-password-request'), # Solicita reset de senha via API
    path('api/confirmreset/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'), # Confirma reset de senha via API
    path('api/gamecards/', GameCardDataView.as_view(), name='gamecard-create'),
    path('api/rankusers/', RankUserListView.as_view(), name='rankuser-list'),
    path('api/user/update/', CustomUserUpdateAPIView.as_view(), name='user-update'),
    ]