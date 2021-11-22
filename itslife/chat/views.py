from .serializers import RoomSerializer, MessageSerializer
from .models import Room, Message
from rest_framework import viewsets, mixins
from .permissions import IsUser

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoomSerializer

    def get_queryset(self):
        user = self.request.user
        rooms = Room.objects.filter(user1=user) | Room.objects.filter(user2=user)
        return rooms

class MessagesView(mixins.RetrieveModelMixin, 
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(room=room_id)