from django.contrib.auth import get_user_model
from django.test import TestCase


UserModel = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = UserModel.objects.create_user(email='user@example.com', password='password123')
        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.role, UserModel.GUEST)

    def test_create_superuser(self):
        admin_user = UserModel.objects.create_superuser(email='admin@example.com', password='admin123')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('admin123'))
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertEqual(admin_user.role, UserModel.GUEST)
