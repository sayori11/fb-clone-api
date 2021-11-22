from django.db import models
from users.models import User

class Room(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.user1}-{self.user2}'

    @property
    def last_msg(self):
        return self.messages.all().last()

class Message(models.Model):
    text = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.id} from {self.sender} in {self.room}'
