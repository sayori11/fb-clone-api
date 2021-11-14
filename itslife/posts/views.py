from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .models import Post, Comment
from users.models import User
from rest_framework.response import Response

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
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, parent_post=post)

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
        serializer.save(author=self.request.user, parent_comment=comment, parent_post = comment.parent_post)

class RepliesDetailViewSet(UpdateView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

