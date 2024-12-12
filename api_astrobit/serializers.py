from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, GameCardData, RankUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializador para retornar informações do usuário.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email']
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
        fields = ['id', 'created_at', 'game_title', 'author_name', 'description']


class RankUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankUser
        fields = ['id', 'player', 'score']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Nenhum usuário associado a este e-mail.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data