from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, MaxLengthValidator
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

    class Meta:
        abstract = True
        managed = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # class Meta:
    #     managed = True
    #     # db_table = 'admin'


class CustomUser(AbstractUser, ModelBase, PermissionsMixin):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    password = models.CharField(
        max_length=255,
        validators=[
        MinLengthValidator(8)
        ],
        blank=False,
    )
    email = models.EmailField(unique=True)
    username = models.CharField(
        unique=True,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(20)
        ]
    )

    def __str__(self):
        return f"{self.username}"

    # class Meta:
    #     managed = True
    #     # db_table = 'users'


class RankUser(ModelBase):
    player = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )
    score = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.player} - {self.score}"

    # class Meta:
    #     managed = True
    #     # db_table = ('rank')


class GameCardData(ModelBase):
    game_title = models.CharField(
        null=False,
        max_length=156,
        blank=False,
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
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

    is_active_game = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.game_title} by {self.author}: {self.description} ({self.link})"

    # class Meta:
    #     managed = True
    #     # db_table = 'game'