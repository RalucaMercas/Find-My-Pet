from django.core.management.base import BaseCommand
from main.models import User
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Add all users with role=Admin to the Admin group"

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        admin_users = User.objects.filter(role=User.Roles.ADMIN)
        for user in admin_users:
            user.groups.add(admin_group)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Added {user.username} to 'Admin' group"))
