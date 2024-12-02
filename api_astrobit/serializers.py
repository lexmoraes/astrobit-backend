from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, GameCardData, RankUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializador para retornar informações do usuário.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Criação de usuário com senha criptografada
        user = CustomUser.objects.create_user(validated_data)
        return user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Criação de usuário com senha criptografada
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)

        # Adicione os campos necessários ao payload
        token['id'] = user.id
        token['name'] = user.name
        token['username'] = user.username
        token['email'] = user.email

        return token


class GameCardDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameCardData
        fields = ['id', 'game_title', 'author', 'description', 'link', 'image']


class RankUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankUser
        fields = ['id', 'placement', 'username', 'score', 'photo_user']