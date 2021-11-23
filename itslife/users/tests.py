from django.test import TestCase
from .models import User

class UserTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="test1@gmail.com", first_name='Test', last_name='User1', password="testpassword1")
        self.user2 = User.objects.create_superuser(email="test2@gmail.com",first_name='Test', last_name='User2', password="testpassword2")

    def test_custom_user(self):
        self.assertFalse(self.user1.is_superuser)
        self.assertTrue(self.user2.is_superuser)
        self.assertEqual(str(self.user1), "Test User1")
        self.assertEqual(str(self.user2), "Test User2")
