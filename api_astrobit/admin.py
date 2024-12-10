from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RankUser, GameCardData

list_per_page = 25


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        label="Nova senha"
    )


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username']
    list_filter = []
    search_fields = ['email', 'username']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'profile_image_url')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
    )

    @admin.action(description="Redefinir senha dos usuários selecionados")
    def reset_password(self, request, queryset):
        # Criação do formulário para redefinição de senha
        form = PasswordResetForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            new_password = form.cleaned_data['new_password']
            for user in queryset:
                user.set_password(new_password)
                user.save()
            self.message_user(request, "Senhas redefinidas com sucesso!")
        else:
            # Retorna a página para entrada da senha
            return admin.helpers.render_action_form(
                request,
                form=form,
                title="Redefinir senha"
            )

    actions = ['reset_password']


@admin.register(RankUser)
class RankUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'placement', 'get_username', 'score', 'created_at')
    search_fields = ('username__username',)
    list_filter = ('placement', 'score')

    def get_username(self, obj):
        return obj.username.username
    get_username.short_description = "Username"


@admin.register(GameCardData)
class GameCardDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'game_title', 'get_username', 'description', 'game_image_url', 'created_at')
    search_fields = ['username__username', 'game_title']
    list_filter = ('created_at',)

    def get_username(self, obj):
        return obj.username  # Ajustado para retornar diretamente a string
    get_username.short_description = "Username"


admin.site.register(CustomUser, CustomUserAdmin)

