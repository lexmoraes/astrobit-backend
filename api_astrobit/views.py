from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import GameCardData, RankUser
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, GameCardDataSerializer, RankUserSerializer


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
            if game.author != request.user:  # Garante que apenas o autor pode deletar
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