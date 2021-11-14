from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer

class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'birthday', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    total_friends = serializers.SerializerMethodField()
    if_friend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'gender', 'bio', 'birthday', 'profile_pic', 'cover_pic', 'total_friends', 'if_friend']
        extra_kwargs = {'password': {'write_only': True}}

    def get_total_friends(self, obj):
        return obj.friends.count()

    def get_if_friend(self, obj):
        current_user = self.context.get('request').user
        return True if current_user in obj.friends.all() else False

class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'birthday', 'profile_pic', 'cover_pic',]
        extra_kwargs = {'password': {'write_only': True}}
