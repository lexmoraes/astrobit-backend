from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
import requests
from django.db import models


# Valida se o link possue extensão de imagem
def validate_image_url(value):
    try:
        response = requests.get(value, stream=True, timeout=5)
        if response.status_code != 200:
            raise ValidationError("A URL da imagem não é válida.")
    except requests.exceptions.Timeout:
        raise ValidationError("A requisição para a URL da imagem excedeu o tempo limite.")
    except requests.exceptions.RequestException as e:
        raise ValidationError(f"Ocorreu um erro na requisição: {str(e)}")


class ModelBase(models.Model):
    id = models.BigAutoField(
        db_column='id',
        null=False,
        primary_key=True,
    )
    created_at = models.DateTimeField(
        db_column='dt_created_at',
        auto_now_add=True,
        verbose_name="Data de Criação",
        null=False,
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified_at',
        auto_now=True,
        verbose_name="Última modificação",
        null=False,
    )
    active = models.BooleanField(
        db_column='cs_active',
        default=True,
        null=False,
    )


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, ModelBase, PermissionsMixin):
    name = models.CharField(max_length=255, default="")
    profile_image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        default="https://raw.githubusercontent.com/alef-monteiro/astrobit-front/refs/heads/develop/src/assets/illustration-game-card.png",
        validators=[validate_image_url],
        verbose_name="Profile Image URL",
        help_text="Insira o link de uma imagem para o perfil."
    )
    password = models.CharField(max_length=255, validators=[
        MinLengthValidator(8)
    ])
    email = models.EmailField(unique=True)
    # Define o campo utilizado como identificador único (username)
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS deve incluir todos os
    # campos obrigatórios ao criar um superusuário, exceto o USERNAME_FIELD e o password
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class RankUser(ModelBase):
    placement = models.PositiveIntegerField(default=0)
    username = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="rank_user_username"
    )
    profile_image_url = models.URLField(
        max_length=500, blank=True, null=True, validators=[validate_image_url]
    )
    score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Preenche profile_image_url com a URL do perfil do CustomUser associado
        if self.username:
            self.profile_image_url = self.username.profile_image_url
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username.username} - {self.placement} - {self.score}"


class GameCardData(ModelBase):
    game_title = models.CharField(max_length=50)
    username = models.CharField()
    description = models.CharField(max_length=255)
    game_image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        default="https://raw.githubusercontent.com/alef-monteiro/astrobit-front/refs/heads/develop/src/assets/illustration-game-card.png",
        validators=[validate_image_url],
        verbose_name="Gamecard Image URL",
        help_text="Insira o link de uma imagem para o gamecard."
    )

    def save(self, *args, **kwargs):
        # Preenche 'username' com o valor de 'CustomUser.username' caso o 'username' ainda não tenha sido fornecido
        if self.username and isinstance(self.username, CustomUser):
            self.username = self.username.username  # Atribui o nome de usuário de CustomUser ao campo username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.game_title
