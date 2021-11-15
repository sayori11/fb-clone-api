from django.db import models
from users.models import User, FriendRequest
from posts.models import Post, Comment

class Notification(models.Model):
    type_choices = (
        ('like', 'like'),
        ('comment', 'comment'),
        ('reply', 'reply'),
        ('share', 'share'),
        ('friend_request', 'friend_request'),
        ('friend_request_accept', 'friend_request_accept'),
        ('message', 'message')
    )

    notification_type = models.CharField(max_length=30, choices=type_choices)
    sent_at = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, on_delete = models.CASCADE)
    to_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='notifications')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, related_name='notification', blank=True, null=True)
    friend_request = models.ForeignKey(FriendRequest, on_delete = models.CASCADE, blank=True, null=True)
    user_has_seen = models.BooleanField(default = False)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.notification_type} from {self.from_user} to {self.to_user}'