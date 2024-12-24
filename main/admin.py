from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import SimpleListFilter
from .models import User
from .forms import AdminUserCreationForm
from django.utils.html import format_html
from .models import LostPost, FoundPost
from django.urls import reverse


class RoleWithoutSuperAdminFilter(SimpleListFilter):
    title = 'role'
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        roles = [
            (User.Roles.NORMAL_USER, 'Normal User'),
            (User.Roles.ADMIN, 'Admin'),
        ]
        return roles

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(role=self.value())
        return queryset


class UserAdmin(BaseUserAdmin):
    base_list_display_superadmin = (
        'id', 'username', 'email', 'role', 'is_staff',
        'first_name', 'last_name', 'country', 'phone_number'
    )
    base_list_display_admin = (
        'id', 'username', 'email', 'role',
        'first_name', 'last_name', 'country', 'phone_number'
    )

    search_fields = ('username', 'email', 'country')
    ordering = ('role', 'id')
    add_form = AdminUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2',
                'first_name', 'last_name', 'email',
                'role', 'phone_number', 'country',
            ),
        }),
    )
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'first_name', 'last_name', 'email',
                'role', 'phone_number', 'country',
            ),
        }),
    )

    def is_request_user_superadmin(self, request):
        return request.user.is_authenticated and hasattr(request.user, 'is_superadmin') and request.user.is_superadmin

    def is_request_user_admin(self, request):
        return request.user.is_authenticated and hasattr(request.user, 'is_admin') and request.user.is_admin

    def get_list_filter(self, request):
        if self.is_request_user_superadmin(request):
            return (RoleWithoutSuperAdminFilter, 'country')
        elif self.is_request_user_admin(request):
            return ('country',)
        return ('country',)

    def get_list_display(self, request):
        if self.is_request_user_superadmin(request):
            return self.base_list_display_superadmin
        elif self.is_request_user_admin(request):
            return self.base_list_display_admin
        return self.base_list_display_admin

    def has_module_permission(self, request):
        return self.is_request_user_superadmin(request) or self.is_request_user_admin(request)

    def has_view_permission(self, request, obj=None):
        return self.is_request_user_superadmin(request) or self.is_request_user_admin(request)

    def has_add_permission(self, request):
        return self.is_request_user_superadmin(request) or self.is_request_user_admin(request)

    def has_change_permission(self, request, obj=None):
        return self.is_request_user_superadmin(request) or self.is_request_user_admin(request)

    def has_delete_permission(self, request, obj=None):
        if self.is_request_user_superadmin(request):
            return True
        if self.is_request_user_admin(request):
            # if obj is None or obj.role == User.Roles.NORMAL_USER:
                return True
        return False

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and not self.is_request_user_superadmin(request) and obj.role == User.Roles.ADMIN:
            new_fieldsets = []
            for title, fields_dict in fieldsets:
                new_fields = [f for f in fields_dict.get('fields', []) if f != 'role']
                new_fieldsets.append((title, {'fields': new_fields}))
            return new_fieldsets
        return fieldsets

    readonly_fields = ('last_login',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        role_field = form.base_fields.get('role')
        if role_field:
            if self.is_request_user_superadmin(request):
                role_field.choices = [
                    (User.Roles.NORMAL_USER, 'Normal User'),
                    (User.Roles.ADMIN, 'Admin'),
                ]
            else:
                role_field.choices = [
                    (User.Roles.NORMAL_USER, 'Normal User'),
                ]
        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request).exclude(role=User.Roles.SUPERADMIN)
        if self.is_request_user_admin(request) and not self.is_request_user_superadmin(request):
            queryset = queryset.filter(role=User.Roles.NORMAL_USER)
        return queryset

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data["password1"])
        obj.save()

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['subtitle'] = ''
        return super().add_view(request, form_url=form_url, extra_context=extra_context)


admin.site.register(User, UserAdmin)

class PostAdminMixin:
    """Mixin to add manage posts functionality for Superadmin."""

    def manage_posts_link(self):
        return format_html(
            '<a class="button" href="{}">Manage Posts</a>',
            reverse('admin_manage_posts')
        )
    manage_posts_link.short_description = "Manage Posts"

class LostPostAdmin(PostAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_archived', 'manage_posts_link')
    list_filter = ('is_archived',)
    search_fields = ('title', 'user__username')

class FoundPostAdmin(PostAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_archived', 'manage_posts_link')
    list_filter = ('is_archived',)
    search_fields = ('title', 'user__username')

admin.site.register(LostPost, LostPostAdmin)
admin.site.register(FoundPost, FoundPostAdmin)

class LostPostAdmin(PostAdminMixin, admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superadmin or request.user.is_admin

class FoundPostAdmin(PostAdminMixin, admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superadmin or request.user.is_admin

