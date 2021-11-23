from django.test import TestCase
from posts.models import Post, Comment
from users.models import User

class TestPost(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test1@gmail.com", first_name='Test', last_name='User1', password="testpassword1")
        self.post = Post.objects.create(text="Test Post", author=self.user)

    def test_setup(self):
        self.assertEqual(self.post.author, self.user)
        self.assertIn(self.post,self.user.posts.all())

    def test_likes_count(self):
        self.post.liked_by.add(self.user)
        self.assertEqual(self.post.likes_count, 1)
        self.assertIn(self.post, self.user.post_likes.all())

    def test_shares_count(self):
        self.post.shared_by.add(self.user)
        self.assertEqual(self.post.shares_count, 1)
        self.assertIn(self.post, self.user.shares.all())

class TestComment(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test1@gmail.com", first_name='Test', last_name='User1', password="testpassword1")
        self.post = Post.objects.create(text="Test Post", author=self.user)
        self.comment = Comment.objects.create(text='Test Comment', author=self.user, parent_post=self.post)
        self.reply = Comment.objects.create(text='Test Reply', author=self.user, parent_post=self.post, parent_comment = self.comment)

    def test_setup(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.parent_post, self.post)
        self.assertEqual(self.reply.parent_comment, self.comment)
        self.assertIn(self.comment,self.post.comments.all())
        self.assertIn(self.reply, self.comment.replies.all())

    def test_likes_count(self):
        self.comment.liked_by.add(self.user)
        self.assertEqual(self.comment.likes_count, 1)

    def test_replies_count(self):    
        self.assertEqual(self.comment.replies_count, 1)

    def test_is_reply(self):
        self.assertTrue(self.reply.is_reply)
        self.assertFalse(self.comment.is_reply)
