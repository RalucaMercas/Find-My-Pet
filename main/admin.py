from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('role', 'id')

    def delete_queryset(self, request, queryset):
        for user in queryset:
            user.groups.clear()
            user.user_permissions.clear()
            user.delete()

admin.site.register(User, UserAdmin)
