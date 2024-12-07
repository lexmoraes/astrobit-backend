from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RankUser, GameCardData


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    @admin.action(description="Redefinir senha dos usuários selecionados")
    def reset_password(modeladmin, request, queryset):
        form = PasswordResetForm(request.POST or None)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            for user in queryset:
                user.set_password(new_password)
                user.save()


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
    ),
    actions = ['reset_password']


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

