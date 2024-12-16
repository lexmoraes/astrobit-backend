from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_astrobit import viewset

router = DefaultRouter()
router.register('users', viewset.CustomUserViewSet)
router.register('game_cards', viewset.GameCardDataViewSet)
router.register('rankusers', viewset.RankUserViewset)
urlpatterns = router.urls

urlpatterns = [

    path('', include(router.urls)),
    path('token/', viewset.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoints da API para login, registro e logout
    path('register/', viewset.RegisterUserViewset.as_view(), name='register'),  # Registro de usuário via API
    path('login/', viewset.LoginUserViewset.as_view(), name='login'),  # Login de usuário via API
    path('logout/', viewset.LogoutUserViewset.as_view(), name='logout'),  # Logout via API
    path('reset/', viewset.PasswordResetRequestViewset.as_view(), name='reset_password_request'),
    # Solicita reset de senha via API
    path('confirmreset/', viewset.PasswordResetConfirmViewset.as_view(), name='reset_password_confirm'),
    # Confirma reset de senha via API
    path('users/{id}/', viewset.CustomUserUpdateAPIViewset.as_view(), name='user_update'),
    path('rankusers/{id}/', viewset.RankUserViewset.as_view({'get': 'list'}), name='rank_user_update'),
    path('api/game_cards/{id}/', viewset.GameCardDataViewSet.as_view({'get': 'list'}), name='game_card_update')
]

urlpatterns += router.urls
