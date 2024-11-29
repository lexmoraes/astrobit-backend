from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, CostumeUserSerializer


class RegisterAPIView(APIView):
    """
    Endpoint para registrar um novo usuário e retornar JWT.
    """

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Criação do usuário
            refresh = RefreshToken.for_user(user)  # Cria o refresh token
            access_token = refresh.access_token  # Cria o access token

            # Retorna os tokens e os dados do usuário
            return Response({
                'user': CostumeUserSerializer(user).data,
                'access': str(access_token),  # Retorna o token de acesso
                'refresh': str(refresh)  # Retorna o refresh token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    Endpoint para login do usuário e retorno de JWT.
    """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)  # Cria o refresh token
            access_token = refresh.access_token  # Cria o access token

            return Response({
                'access': str(access_token),  # Retorna o token de acesso
                'refresh': str(refresh)  # Retorna o refresh token
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    """
    Endpoint para logout (revogar o refresh token).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()  # Opcional: Deletar token se for usado TokenAuthentication
        except AttributeError:
            pass

        # Invalida o refresh token removendo-o da blacklist (caso você esteja utilizando blacklist de refresh tokens)
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Marca o token como inválido
            return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
