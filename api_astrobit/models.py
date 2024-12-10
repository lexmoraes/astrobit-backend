from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.sites import requests
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


# Valida se o link possue extensão de imagem
def validate_image_url(value):
    try:
        response = requests.head(value, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image'):
            raise ValidationError('A URL fornecida não parece ser de uma imagem.')
    except Exception:
        raise ValidationError('Não foi possível verificar a URL fornecida.')


class ModelBase(models.Model):
    id = models.BigAutoField(
        db_column='id',
        null=False,
        primary_key=True,
    )
    created_at = models.DateTimeField(
        db_column='dt_created_at',
        auto_now_add=True,
        null=False,
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified_at',
        auto_now=True,
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
        CustomUser, on_delete=models.CASCADE
    )
    profile_image_url = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE
    )
    score = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.username.username, self.placement, self.score


class GameCardData(ModelBase):
    game_title = models.CharField(max_length=255)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    game_image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        validators=[validate_image_url],
        verbose_name="Gamecard Image URL",
        help_text="Insira o link de uma imagem para o gamecardg."
    )

    def __str__(self):
        return self.game_title