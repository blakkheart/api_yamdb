from django.contrib import admin

from user.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Register User model in Admin panel with all fields."""

    fieldsets = (
        (
            'Standard info',
            {
                'fields': (
                    'email',
                    'username',
                    'password',
                    'first_name',
                    'last_name',
                )
            },
        ),
        ('Extra Fields', {'fields': ('bio', 'role',)}),
    )
