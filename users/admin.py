from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Payment
from django.utils.translation import gettext_lazy as _



class CustomUserAdmin(UserAdmin):
    # Убираем username из отображения
    list_display = ('email', 'first_name', 'last_name', 'phone', 'city', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'city')
    ordering = ('email',)

    # Поля в форме редактирования
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'city', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Поля при создании нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # Поиск
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'city')


# Регистрируем CustomUser с кастомным админом
admin.site.register(CustomUser, CustomUserAdmin)


# Админка для Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'paid_course', 'paid_lesson', 'payment_date']
    list_filter = ['payment_method', 'payment_date', 'paid_course', 'paid_lesson']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['payment_date']