from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ['date_joined', 'last_modified', 'last_login']
    ordering = ('email',)
    fieldsets = (
        ('Registration Information', {'fields': ('email', 'username', 'password', 'last_login', 'date_joined', 'last_modified')}),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
        ('Permissions Information', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(User, CustomUserAdmin)