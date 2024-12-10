# Generated by Django 5.1.1 on 2024-12-10 18:16

import api_astrobit.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_astrobit', '0002_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamecarddata',
            old_name='author',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='gamecarddata',
            name='image',
        ),
        migrations.RemoveField(
            model_name='gamecarddata',
            name='link',
        ),
        migrations.RemoveField(
            model_name='rankuser',
            name='photo_user',
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_image_url',
            field=models.URLField(blank=True, default='https://raw.githubusercontent.com/alef-monteiro/astrobit-front/refs/heads/develop/src/assets/illustration-game-card.png', help_text='Insira o link de uma imagem para o perfil.', max_length=500, null=True, validators=[api_astrobit.models.validate_image_url], verbose_name='Profile Image URL'),
        ),
        migrations.AddField(
            model_name='gamecarddata',
            name='game_image_url',
            field=models.URLField(blank=True, default='https://raw.githubusercontent.com/alef-monteiro/astrobit-front/refs/heads/develop/src/assets/illustration-game-card.png', help_text='Insira o link de uma imagem para o gamecardg.', max_length=500, null=True, validators=[api_astrobit.models.validate_image_url], verbose_name='Gamecard Image URL'),
        ),
        migrations.AddField(
            model_name='rankuser',
            name='profile_image_url',
            field=models.ForeignKey(default=123456, on_delete=django.db.models.deletion.CASCADE, related_name='rank_user_profile_image', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='modelbase',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='dt_created_at', verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='modelbase',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, db_column='dt_modified_at', verbose_name='Última modificação'),
        ),
        migrations.AlterField(
            model_name='rankuser',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rank_user_username', to=settings.AUTH_USER_MODEL),
        ),
    ]