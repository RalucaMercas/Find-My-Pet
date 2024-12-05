from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import AdminUserCreationForm


class UserAdmin(BaseUserAdmin):
    # Displayed fields in the list view
    list_display = ('id', 'username', 'email', 'role', 'is_staff', 'first_name', 'last_name', 'country', 'phone_number')
    list_filter = ('role', 'is_staff', 'country')
    search_fields = ('username', 'email', 'country')
    ordering = ('role', 'id')

    # Use a custom form for adding users
    add_form = AdminUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2',  # Include password fields
                'first_name', 'last_name', 'email',
                'role', 'phone_number', 'country',
            ),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        """
        Customize fieldsets dynamically based on whether it's a new or existing user.
        """
        if obj:  # Editing an existing user
            return (
                (None, {
                    'fields': (
                        'username', 'first_name', 'last_name',
                        'email', 'phone_number', 'country', 'role',
                    ),
                }),
            )
        else:  # Adding a new user
            return self.add_fieldsets

    readonly_fields = ('last_login',)

    def get_form(self, request, obj=None, **kwargs):
        """
        Restrict available roles dynamically when adding users.
        """
        form = super().get_form(request, obj, **kwargs)
        if obj:  # Editing an existing user
            role_field = form.base_fields.get('role')
            if role_field:
                role_field.choices = [
                    (User.Roles.NORMAL_USER, 'Normal User'),
                    (User.Roles.ADMIN, 'Admin'),
                ]
        else:  # Adding a new user
            role_field = form.base_fields.get('role')
            if role_field:
                role_field.choices = [
                    (User.Roles.NORMAL_USER, 'Normal User'),
                    (User.Roles.ADMIN, 'Admin'),
                ]
        return form

    def save_model(self, request, obj, form, change):
        """
        Ensure passwords are hashed before saving the user.
        """
        if not change:  # Only for new users
            obj.set_password(form.cleaned_data["password1"])
        obj.save()

    def add_view(self, request, form_url='', extra_context=None):
        """
        Customize the add view to remove the default help text.
        """
        extra_context = extra_context or {}
        extra_context['subtitle'] = ''  # Remove or replace the subtitle
        return super().add_view(request, form_url, extra_context)


admin.site.register(User, UserAdmin)
