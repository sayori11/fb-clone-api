from rest_framework import serializers
from .models import Room, Message
from users.serializers import UserPreviewSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserPreviewSerializer(read_only=True, many=False)

    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'sent_at']

class RoomSerializer(serializers.ModelSerializer):
    last_msg = serializers.SerializerMethodField()
    user1 = UserPreviewSerializer(read_only=True, many=False)
    user2 = UserPreviewSerializer(read_only=True, many=False)

    class Meta:
        model = Room
        fields = ['id', 'user1', 'user2', 'created_at', 'last_msg']

    def get_last_msg(self,obj):
        last = obj.last_msg
        return MessageSerializer(last)

