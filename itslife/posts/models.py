from django.db import models
from users.models import User

class Content(models.Model):
    text = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to = 'post_pics')
    video = models.FileField(blank=True, null=True, upload_to = 'post_videos')
    posted_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    isEdited = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def likes_count(self):
        return self.liked_by.count()


class Post(Content):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='posts')
    liked_by = models.ManyToManyField(User, blank=True, related_name='post_likes')
    shared_by = models.ManyToManyField(User, blank=True, related_name='shares')

    class Meta:
        ordering = ('-posted_at',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'{self.id}'

    @property
    def shares_count(self):
        return self.shared_by.count()

class Comment(Content):
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete = models.CASCADE, related_name='replies', blank=True, null=True)
    liked_by = models.ManyToManyField(User, blank=True, related_name='comment_likes')

    class Meta:
        ordering = ('-posted_at',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.id}'

    @property
    def replies_count(self):
        try:
            return self.reply.count()
        except:
            return 0

    @property
    def is_reply(self):
        return False if self.parent_comment is None else True

