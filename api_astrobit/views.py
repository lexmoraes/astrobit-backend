from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import GameCardData, RankUser, CustomUser
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, GameCardDataSerializer, \
    RankUserSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, CustomUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully', 'user': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retorna o usuário autenticado
        return self.request.user


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                # Gerar token JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutUserView(APIView):
    permission_classes = [AllowAny]
    """
    Endpoint para logout do usuário (revogação do token).
    """

    def post(self, request):
        request.user.auth_token.delete()  # Deleta o token associado ao usuário
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
            )

            send_mail(
                'Redefinição de Senha',
                f'Use este link para redefinir sua senha: {reset_url}',
                'seu_email@dominio.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "E-mail de redefinição enviado com sucesso."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError("Token inválido ou expirado.")

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise ValidationError("Token inválido ou expirado.")

        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameCardDataView(APIView):
    """
    Classe para gerenciar os dados de GameCardData: Listar, Criar, Atualizar e Deletar.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]  # Permite leitura sem autenticação, mas exige autenticação para escrita

    def get(self, request, pk=None):
        """
        Recupera todos os registros ou um específico (se o pk for fornecido).
        """
        if pk:
            try:
                game = GameCardData.objects.get(pk=pk)
                serializer = GameCardDataSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except GameCardData.DoesNotExist:
                return Response({'error': 'GameCardData não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        games = GameCardData.objects.all()
        serializer = GameCardDataSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Cria um novo registro de GameCardData. Apenas usuários autenticados podem criar.
        """
        serializer = GameCardDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # Define o usuário autenticado como autor
            return Response({'message': 'GameCardData criado com sucesso', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Atualiza um registro específico de GameCardData. Apenas o autor pode atualizar.
        """
        try:
            game = GameCardData.objects.get(pk=pk)
            if game.author != request.user:  # Garante que apenas o autor pode editar
                return Response({'error': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)
        except GameCardData.DoesNotExist:
            return Response({'error': 'GameCardData não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GameCardDataSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'GameCardData atualizado com sucesso', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deleta um registro específico de GameCardData. Apenas o autor pode deletar.
        """
        try:
            game = GameCardData.objects.get(pk=pk)
            if game.username != request.user:  # Garante que apenas o autor pode deletar
                return Response({'error': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)
            game.delete()
            return Response({'message': 'GameCardData deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except GameCardData.DoesNotExist:
            return Response({'error': 'GameCardData não encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class RankUserListView(APIView):
    def get(self, request):
        rank_users = RankUser.objects.all()
        serializer = RankUserSerializer(rank_users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RankUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)