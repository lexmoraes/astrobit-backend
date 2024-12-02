from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RankUser, GameCardData


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username']
    list_filter = []
    search_fields = ['email', 'username']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
    )


# Registro do modelo RankUser
@admin.register(RankUser)
class RankUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'placement', 'username', 'score', 'created_at')
    search_fields = ('username__username',)
    list_filter = ('placement', 'score')

# Registro do modelo GameCardData
@admin.register(GameCardData)
class GameCardDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'game_title', 'author', 'description', 'link', 'created_at')
    search_fields = ('game_title', 'author__username', 'description')
    list_filter = ('created_at',)


admin.site.register(CustomUser, CustomUserAdmin)

