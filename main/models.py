from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


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


class BasePost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_posts',
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    area = models.CharField(max_length=255)
    PET_TYPE_CHOICES = [
        ('cat', 'Cat'),
        ('dog', 'Dog'),
        ('other', 'Other'),
    ]
    pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    images = GenericRelation('PetImage')
    is_archived = models.BooleanField(default=False)

    class Meta:
        abstract = True  # This model will not create its own table
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class LostPost(BasePost):
    pet_name = models.CharField(max_length=255)
    date_lost = models.DateField()

    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    pet_sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    reward = models.PositiveIntegerField(
        blank=True, null=True, help_text="Enter a reward amount (whole number) or leave blank."
    )


class FoundPost(BasePost):
    date_found = models.DateField()


class PetImage(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    post = GenericForeignKey('content_type', 'object_id')  # Generic relation to either LostPost or FoundPost
    image = models.ImageField(upload_to='pet_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for post: {self.post}"
