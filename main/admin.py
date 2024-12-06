from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import AdminUserCreationForm


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_staff', 'first_name', 'last_name', 'country', 'phone_number')
    list_filter = ('role', 'is_staff', 'country')
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

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (None, {
                    'fields': (
                        'username', 'first_name', 'last_name',
                        'email', 'phone_number', 'country', 'role',
                    ),
                }),
            )
        else:
            return self.add_fieldsets

    readonly_fields = ('last_login',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            role_field = form.base_fields.get('role')
            if role_field:
                role_field.choices = [
                    (User.Roles.NORMAL_USER, 'Normal User'),
                    (User.Roles.ADMIN, 'Admin'),
                ]
        else:
            role_field = form.base_fields.get('role')
            if role_field:
                role_field.choices = [
                    (User.Roles.NORMAL_USER, 'Normal User'),
                    (User.Roles.ADMIN, 'Admin'),
                ]
        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(role=User.Roles.SUPERADMIN)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data["password1"])
        obj.save()

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['subtitle'] = ''
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

admin.site.register(User, UserAdmin)

