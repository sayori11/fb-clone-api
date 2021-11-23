from django.test import TestCase
from .models import Notification
from users.models import User

class NotificationTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(email="test1@gmail.com", first_name='Test', last_name='User1', password="testpassword1")
        self.user2 = User.objects.create_user(email="test2@gmail.com",first_name='Test', last_name='User2', password="testpassword2")
        self.notif = Notification.objects.create(notification_type='like', from_user=self.user1, to_user=self.user2)

    def test_setUp(self):
        self.assertEqual(str(self.notif), f'like from {self.user1} to {self.user2}')
