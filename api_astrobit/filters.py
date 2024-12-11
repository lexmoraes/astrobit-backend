import django_filters
from django_filters import rest_framework as filters
from api_astrobit.models import CustomUser, GameCardData, RankUser


class CustomUserFilter(filters.FilterSet):
    """
    Filtros para o modelo CustomUser.
    """
    email = filters.CharFilter(lookup_expr='icontains')  # Filtra por email com busca parcial
    name = filters.CharFilter(lookup_expr='icontains')  # Filtra por nome com busca parcial
    active = filters.BooleanFilter()  # Filtra por usuários ativos/inativos

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'active']  # Campos disponíveis para filtragem


class GameCardDataFilter(filters.FilterSet):
    """
    Filtros para o modelo GameCardData.
    """
    game_title = filters.CharFilter(lookup_expr='icontains')  # Busca parcial por título do jogo
    author_name = filters.CharFilter(field_name='author__username', lookup_expr='icontains')  # Filtra pelo username do autor
    created_at = filters.DateFromToRangeFilter()  # Filtra por intervalo de datas de criação

    class Meta:
        model = GameCardData
        fields = ['game_title', 'author_name', 'created_at']  # Campos disponíveis para filtragem


class RankUserFilter(django_filters.FilterSet):
    score = django_filters.NumberFilter(field_name='score', lookup_expr='gte')

    class Meta:
        model = RankUser
        fields = ['player', 'score']