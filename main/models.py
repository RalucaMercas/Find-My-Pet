from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


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
        unique=True,
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


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pet_name = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    date_lost = models.DateField()

    PET_TYPE_CHOICES = [
        ('cat', 'Cat'),
        ('dog', 'Dog'),
        ('other', 'Other'),
    ]
    pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES)
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    pet_sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    reward = models.PositiveIntegerField(
        blank=True, null=True, help_text="Enter a reward amount (whole number) or leave blank."
    )
    class Meta:
        ordering = ['-created_at']  # Default ordering: newest posts first

    def __str__(self):
        return self.title
