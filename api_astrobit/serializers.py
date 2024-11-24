from rest_framework import serializers
from .models import CustomUser

class CostumeUserSerializer(serializers.ModelSerializer):
    """
    Serializador para retornar informações do usuário.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username']

class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializador para registrar novos usuários.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        """
        Cria um novo usuário utilizando o gerenciador.
        """
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
