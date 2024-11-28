from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField


class User(AbstractUser):
    class Roles(models.TextChoices):
        NORMAL_USER = 'Normal'
        ADMIN = 'Admin'
        SUPERADMIN = 'SuperAdmin'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.NORMAL_USER,
    )

    phone_number = PhoneNumberField(
        help_text="Provide a valid phone number, including the country code."
    )

    country = CountryField()  # Stores the country as ISO alpha-2 code

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.role == self.Roles.SUPERADMIN:
            self.is_superuser = True
            self.is_staff = True
        elif self.role == self.Roles.ADMIN:
            self.is_superuser = False
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
        super().save(*args, **kwargs)

    def is_admin(self):
        return self.role == self.Roles.ADMIN

    def is_superadmin(self):
        return self.role == self.Roles.SUPERADMIN

    def is_normal_user(self):
        return self.role == self.Roles.NORMAL_USER
