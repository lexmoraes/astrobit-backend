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
    score = models.PositiveIntegerField(default=0)
    photo_user = models.ImageField(default='None', upload_to='photos')

    def __str__(self):
        return self.username.username


class GameCardData(ModelBase):
    game_title = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    link = models.URLField(max_length=150)
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.game_title