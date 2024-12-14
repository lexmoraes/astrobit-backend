from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from api_astrobit import serializers, models, filters


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer
    filterset_class = filters.CustomUserFilter


class GameCardDataViewSet(viewsets.ModelViewSet):
    queryset = models.GameCardData.objects.all()
    serializer_class = serializers.GameCardDataSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = filters.GameCardDataFilter
    ordering_fields = ['game_title', 'author', 'id']

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied("Você não tem permissão para alterar este objeto.")

        request.data['author'] = request.user
        return self.update(request, *args, **kwargs)


class RankUserViewSet(viewsets.ModelViewSet):
    queryset = models.RankUser.objects.all()
    serializer_class = serializers.RankUserSerializer
