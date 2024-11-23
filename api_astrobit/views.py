from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer, CostumeUserSerializer

class SignUpAPIView(APIView):
    """
    Endpoint para registrar novos usuários.
    """
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': CostumeUserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    """
    Endpoint para autenticação de usuários (login).
    """
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    """
    Endpoint para logout do usuário (revogação do token).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Deleta o token associado ao usuário
        return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)
