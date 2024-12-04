from django.core.management.base import BaseCommand
from main.models import User


class Command(BaseCommand):
    help = 'Create the default SuperAdmin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(role=User.Roles.SUPERADMIN).exists():
            User.objects.create_user(
                username='superadmin',
                email='superadmin@example.com',
                password='supersecurepassword',
                role=User.Roles.SUPERADMIN,
            )
            self.stdout.write(self.style.SUCCESS('SuperAdmin created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('SuperAdmin already exists.'))
