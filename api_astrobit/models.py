from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models


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
    player = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="rank_users"
    )
    score = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.player.username} - {self.score}"


class GameCardData(ModelBase):
    game_title = models.CharField(
        null=False,
        max_length=156,
        blank=False,
    )
    author_name = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
        related_name="game_cards"
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=255
    )
    link = models.URLField(
        null=False,
        blank=False,
        help_text="Insira o link do jogo."
    )

    def __str__(self):
        return self.game_title, self.author_name.username, self.description, self.link