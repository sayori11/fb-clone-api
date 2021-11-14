from rest_framework import serializers
from .models import Post, Comment
from users.models import User
from users.serializers import UserSerializer

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    likes_count = serializers.SerializerMethodField(read_only=True)
    replies_count = serializers.SerializerMethodField(read_only=True)
    if_liked = serializers.SerializerMethodField(read_only=True)
    replies = RecursiveField(read_only=True, many=True)

    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'image', 'video', 'posted_at', 'edited_at', 'isEdited', 'author', 'liked_by','likes_count', 'replies_count', 'if_liked', 'replies']

    def get_likes_count(self, obj):
        return obj.likes_count

    def get_replies_count(self, obj):
        return obj.replies_count

    def get_if_liked(self, obj):
        current_user = self.context.get('request').user
        return True if current_user in obj.liked_by.all() else False


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    shares_count = serializers.SerializerMethodField(read_only=True)
    if_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'video', 'posted_at', 'edited_at', 'isEdited', 'author', 'liked_by', 'shared_by', 'likes_count', 'comments_count', 'shares_count', 'comments', 'if_liked']

    def get_likes_count(self, obj):
        return obj.likes_count

    def get_comments_count(self,obj):
        return obj.comments.count()

    def get_shares_count(self, obj):
        return obj.shares_count

    def get_if_liked(self, obj):
        current_user = self.context.get('request').user
        return True if current_user in obj.liked_by.all() else False




    

