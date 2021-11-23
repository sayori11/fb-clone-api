from rest_framework import viewsets, generics, views, status
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .models import Post, Comment
from notifications.models import Notification
from users.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class UpdateView:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        post = self.get_object()
        data = request.data
        data['isEdited'] = True
        serializer = self.get_serializer(post, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PostsViewset(UpdateView, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        current_user = self.request.user
        friends = current_user.friends.all()
        posts = Post.objects.filter(author__in = friends)|Post.objects.filter(author=current_user)
        return posts
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserPostsViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=user)
        shared_posts = user.shares.all()
        return posts|shared_posts

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CommentsListViewSet(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        comments = Comment.objects.filter(parent_post=post_id)
        main_comments = [comment for comment in comments if comment.is_reply is False]
        return main_comments

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        user = self.request.user
        post = Post.objects.get(id=post_id)
        notif = Notification.objects.create(notification_type='comment', from_user=user, to_user=post.author)
        serializer.save(author=self.request.user, parent_post=post, notification=[notif])

class CommentsDetailViewSet(UpdateView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]


class RepliesListViewSet(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        replies = Comment.objects.filter(parent_comment=comment_id)
        return replies

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        comment_id = self.kwargs['comment_id']
        comment = Comment.objects.get(id=comment_id)
        notif = Notification.objects.create(notification_type='reply', from_user=self.request.user, to_user=comment.author)
        serializer.save(author=self.request.user, parent_comment=comment, parent_post = comment.parent_post, notification = [notif] )
        

class RepliesDetailViewSet(UpdateView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

class LikePostView(views.APIView):
    
    def post(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        
        if user in post.liked_by.all():
            post.liked_by.remove(user)
            return Response({"response":"Unliked the post", "likes_count":post.likes_count}, status=status.HTTP_200_OK)
        
        post.liked_by.add(user)
        Notification.objects.create(notification_type='like', from_user=user, to_user=post.author, post=post)
        return Response({"response":"Liked the post", "likes_count":post.likes_count}, status=status.HTTP_200_OK)

class LikeCommentView(views.APIView):

    def post(self, request, post_id, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id,)
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if comment.parent_post != post:
            return Response({"response":"Comment and post do not match"}, status = status.HTTP_400_BAD_REQUEST)
        if user in comment.liked_by.all():
            comment.liked_by.remove(user)
            return Response({"response":"Unliked the comment", "likes_count":comment.likes_count}, status=status.HTTP_200_OK)

        comment.liked_by.add(user)
        Notification.objects.create(notification_type='like', from_user=user, to_user=post.author, comment=comment)
        return Response({"response":"Liked the comment", "likes_count":comment.likes_count}, status=status.HTTP_200_OK)

class SharePostView(views.APIView):

    def post(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        post.shared_by.add(user)
        Notification.objects.create(notification_type='share', from_user=user, to_user=post.author, post=post)
        return Response({"response":"Shared the post", "shares_count":post.shares_count}, status=status.HTTP_200_OK)