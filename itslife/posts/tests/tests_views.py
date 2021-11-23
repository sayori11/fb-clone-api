from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from posts.models import Post, Comment
from users.models import User 

class TestPost(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email="test1@gmail.com", first_name='Test', last_name='User1', password="testpassword1")
        self.user2 = User.objects.create_user(email="test2@gmail.com", first_name='Test', last_name='User2', password="testpassword2")
        self.post = Post.objects.create(text="Test Post 1", author=self.user1)
        self.user1.friends.add(self.user2)
        self.friend_post = Post.objects.create(text="Test Post 2", author=self.user2)
        connection_data = {'email':'test1@gmail.com', 'password': 'testpassword1'}
        token = self.client.post('/api/v1/auth/token/login', connection_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.data['auth_token'])

    def test_posts_list(self):
        response = self.client.get("/api/v1/posts/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_posts_detail(self):
        response = self.client.get("/api/v1/posts/"+str(self.post.id)+"/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Test Post 1")

    def test_posts_add(self):
        post_data = {
            "text" : "Test Post Add"
        }
        response = self.client.post("/api/v1/posts/", post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)

    def test_posts_edit(self):
        post_data = {
            "text" : "Test Post Edit"
        }
        response = self.client.put("/api/v1/posts/"+str(self.post.id)+"/", post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['isEdited'])
        self.assertEqual(response.data['text'], post_data['text'])

    def test_posts_delete(self):
        posts_no = Post.objects.count()
        response = self.client.delete("/api/v1/posts/"+str(self.post.id)+"/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), posts_no-1)
        
    def test_user_posts(self):
        response = self.client.get("/api/v1/posts/user/"+str(self.user1.id)+"/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class TestComment(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email="test1@gmail.com", first_name='Test', last_name='User1', password="testpassword1")
        self.user2 = User.objects.create_user(email="test2@gmail.com", first_name='Test', last_name='User2', password="testpassword2")
        self.post = Post.objects.create(text="Test Post 1", author=self.user1)
        self.comment = Comment.objects.create(text="Test Comment 1", author=self.user1, parent_post=self.post)
        connection_data = {'email':'test1@gmail.com', 'password': 'testpassword1'}
        token = self.client.post('/api/v1/auth/token/login', connection_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.data['auth_token'])

    def test_comments_list(self):
        response = self.client.get("/api/v1/posts/" + str(self.post.id) + "/comments/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_comments_detail(self):
        response = self.client.get("/api/v1/posts/"+str(self.post.id)+"/comments/" + str(self.comment.id)+'/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Test Comment 1")

    def test_comments_add(self):
        comment_data = {
            "text" : "Test Comment Add"
        }
        response = self.client.post("/api/v1/posts/" + str(self.post.id) + "/comments/", comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_posts_edit(self):
        comment_data = {
            "text" : "Test Comment Edit"
        }
        response = self.client.put("/api/v1/posts/"+str(self.post.id)+"/comments/" + str(self.comment.id)+'/', comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['isEdited'])
        self.assertEqual(response.data['text'], comment_data['text'])

    def test_comments_delete(self):
        comments_no = Comment.objects.count()
        response = self.client.delete("/api/v1/posts/"+str(self.post.id)+"/comments/" + str(self.comment.id)+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), comments_no-1)
    
    def test_replies_add(self):
        reply_data = {
            "text" : "Test Reply Add"
        }
        response = self.client.post("/api/v1/posts/comments/" + str(self.comment.id) + "/replies/", reply_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.comment.replies_count, 1)


    def test_replies_list(self):
        response = self.client.get("/api/v1/posts/comments/" + str(self.comment.id) + "/replies/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class TestLikeUnlikeShare(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email="test1@gmail.com", first_name='Test', last_name='User1', password="testpassword1")
        self.user2 = User.objects.create_user(email="test2@gmail.com", first_name='Test', last_name='User2', password="testpassword2")
        self.post = Post.objects.create(text="Test Post 1", author=self.user1)
        self.comment = Comment.objects.create(text="Test Comment 1", author=self.user1, parent_post=self.post)
        connection_data = {'email':'test1@gmail.com', 'password': 'testpassword1'}
        token = self.client.post('/api/v1/auth/token/login', connection_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.data['auth_token'])

    def test_like_unlike_posts(self):
        response = self.client.post("/api/v1/posts/" + str(self.post.id) + "/like/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"response":"Liked the post", "likes_count":1})
        unlike_response = self.client.post("/api/v1/posts/" + str(self.post.id) + "/like/", format='json')
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unlike_response.data, {"response":"Unliked the post", "likes_count":0})

    def test_like_unlike_comments(self):
        response = self.client.post("/api/v1/posts/" +str(self.post.id)+"/comments/" + str(self.comment.id)+"/like/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"response":"Liked the comment", "likes_count":1})
        unlike_response = self.client.post("/api/v1/posts/" +str(self.post.id)+"/comments/" + str(self.comment.id)+"/like/", format='json')
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unlike_response.data, {"response":"Unliked the comment", "likes_count":0})

    def test_shares(self):
        response = self.client.post("/api/v1/posts/" + str(self.post.id) + "/share/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"response":"Shared the post", "shares_count":1})



        

