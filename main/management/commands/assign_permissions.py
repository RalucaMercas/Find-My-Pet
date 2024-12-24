from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from main.models import LostPost, FoundPost

class Command(BaseCommand):
    help = 'Assign delete permissions for LostPost and FoundPost to Admin group'

    def handle(self, *args, **kwargs):
        admin_group, created = Group.objects.get_or_create(name='Admin')

        for model in [LostPost, FoundPost]:
            content_type = ContentType.objects.get_for_model(model)
            delete_permission = Permission.objects.get(
                codename=f'delete_{model._meta.model_name}',
                content_type=content_type
            )
            admin_group.permissions.add(delete_permission)

        self.stdout.write(self.style.SUCCESS('Permissions assigned successfully'))
