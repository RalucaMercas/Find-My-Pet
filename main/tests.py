from django.test import TestCase
from .models import User


class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(username="dorel", role=User.Roles.NORMAL_USER)
        self.assertEqual(user.username, "dorel")
        self.assertEqual(user.role, User.Roles.NORMAL_USER)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        admin_user = User.objects.create(username="maricica", role=User.Roles.ADMIN)
        self.assertEqual(admin_user.username, "maricica")
        self.assertEqual(admin_user.role, User.Roles.ADMIN)
        self.assertTrue(admin_user.is_staff)
        self.assertFalse(admin_user.is_superuser)

        superadmin_user = User.objects.create(username="lenutza", role=User.Roles.SUPERADMIN)
        self.assertEqual(superadmin_user.username, "lenutza")
        self.assertEqual(superadmin_user.role, User.Roles.SUPERADMIN)
        self.assertTrue(superadmin_user.is_staff)
        self.assertTrue(superadmin_user.is_superuser)

        users = User.objects.all()
        for user in users:
            print(user.username, user.role, "Is staff:", user.is_staff, "Is superuser:", user.is_superuser)
