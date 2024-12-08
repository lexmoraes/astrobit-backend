from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api_astrobit.filters import CustomUserFilter, GameCardDataFilter
from api_astrobit.models import CustomUser, GameCardData, RankUser
from api_astrobit.serializers import CustomUserSerializer, GameCardDataSerializer, RankUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomUserFilter


class GameCardDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar as operações CRUD de GameCardData.
    """

    queryset = GameCardData.objects.all()
    serializer_class = GameCardDataSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GameCardDataFilter
    search_fields = ['game_title', 'description', 'author__username']
    ordering_fields = ['game_title', 'author', 'id']


def perform_create(self, serializer):
    """
    Sobrescreve o método para definir o autor como o usuário autenticado.
    """
    serializer.save(author=self.request.user)


def get_queryset(self):
    """
    Sobrescreve o queryset para filtrar por autor autenticado (opcional).
    """
    if self.request.user.is_authenticated:
        return GameCardData.objects.filter(author=self.request.user)
    return GameCardData.objects.all()


class RankUserViewSet(ModelViewSet):
    queryset = RankUser.objects.all()
    serializer_class = RankUserSerializer
