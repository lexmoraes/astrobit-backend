from django.contrib.auth import get_user_model, tokens, authenticate
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import viewsets, status, mixins
from rest_framework import exceptions, generics, permissions, response, serializers
from rest_framework.views import APIView
from rest_framework_simplejwt import views
from rest_framework_simplejwt.tokens import RefreshToken

from api_astrobit import serializers, models, filters


User = get_user_model()  # Garantir uso do modelo de usuário personalizado (CustomUser, se houver)

class CustomTokenObtainPairView(views.TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


class RegisterUserViewset(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response.Response(
                {
                    'message': 'Usuário criado com sucesso',
                    'user': serializer.data
                },
                status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserUpdateAPIViewset(generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retorna o usuário autenticado
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class LoginUserViewset(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                # Gerar token JWT
                refresh = RefreshToken.for_user(user)
                return response.Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            return response.Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return response.Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutUserViewset(APIView):
    permission_classes = [permissions.AllowAny]
    """
    Endpoint para logout do usuário (revogação do token).
    """

    def post(self, request):
        request.user.auth_token.delete()  # Deleta o token associado ao usuário
        return response.Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class PasswordResetRequestViewset(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = serializers.PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token_generator = tokens.PasswordResetTokenGenerator()
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
            return response.Response({"message": "E-mail de redefinição enviado com sucesso."}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmViewset(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise exceptions.ValidationError("Token inválido ou expirado.")

        token_generator = tokens.PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise exceptions.ValidationError("Token inválido ou expirado.")

        serializer = serializers.PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return response.Response({
                "message": "Senha redefinida com sucesso."
            },
            status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer
    filterset_class = filters.CustomUserFilter


class GameCardDataViewSet(viewsets.ModelViewSet):
    queryset = models.GameCardData.objects.all()
    serializer_class = serializers.GameCardDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = filters.GameCardDataFilter

    # def create(self, request, *args, **kwargs):
    #     request.data['author'] = request.user
    #     return super().create(request, *args, **kwargs)
    #
    # def put(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if instance.author != request.user:
    #         raise exceptions.PermissionDenied("Você não tem permissão para alterar este objeto.")
    #
    #     request.data['author'] = request.user
    #     return self.update(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if instance.author != request.user:
    #         raise exceptions.PermissionDenied("Você não tem permissão para alterar este objeto.")
    #
    #     request.data['author'] = request.user
    #     return self.update(request, *args, **kwargs)


class RankUserViewset(viewsets.ModelViewSet):

    queryset = models.RankUser.objects.all()
    serializer_class = serializers.RankUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        # Retorna o usuário autenticado
        return self.request.user
    #
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    #
    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return response.Response(serializer.data)
    #
    #
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return response.Response(serializer.data)