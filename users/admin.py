from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    # Убираем username из отображаемых полей
    list_display = ('email', 'first_name', 'last_name', 'phone', 'city', 'is_staff')

    # Обновляем fieldsets - убираем username
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'city', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Обновляем add_fieldsets - убираем username
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # Убираем сортировку по username и ставим по email
    ordering = ('email',)

    # Указываем поля для поиска
    search_fields = ('email', 'first_name', 'last_name', 'phone')


admin.site.register(CustomUser, CustomUserAdmin)
