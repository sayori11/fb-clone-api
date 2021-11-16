from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, UserEditSerializer ,FriendRequestSerializer
from .models import User, FriendRequest
from notifications.models import Notification
from .permissions import IsUserOrReadOnly
import requests

class UsersDetailView(mixins.RetrieveModelMixin, 
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsUserOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserEditSerializer
        else:
            return UserSerializer
        return serializers.Default

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ActivateUser(APIView):

    def get(self, request, uid, token, format = None):
        payload = {'uid': uid, 'token': token}

        url = 'http://127.0.0.1:8000/api/v1/auth/users/activation/'
        response = requests.post(url, data = payload)

        if response.status_code == 204:
            return Response({'detail': 'Activated successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response(response.json())

class FriendRequestView(APIView):

    def post(self, request, user_id, format = None):
        sender = request.user
        receiver = get_object_or_404(User, id=user_id)
        if receiver in sender.friends.all():
            return Response({"response": "Already friends"})
        fr, get = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
        if not get:
            return Response({"response": "Friend request sent already"})
        Notification.objects.create(notification_type='friend_request', from_user=sender, to_user=receiver, friend_request= fr)
        return Response({"response":"Friend request sent successfully!"}, status=status.HTTP_200_OK)

class FriendRequestResponseView(APIView):

    def post(self, request, friendrequest_id, response_msg, format = None):
        friend_request = get_object_or_404(FriendRequest, id=friendrequest_id)
        sender = friend_request.sender
        receiver = friend_request.receiver
        if request.user == receiver:
            if response_msg == "accept":
                friend_request.receiver.friends.add(sender)
                friend_request.delete()
                Notification.objects.create(notification_type='friend_request_accept', from_user=receiver, to_user=sender)
                return Response({"response":"Friend request accepted"},status=status.HTTP_200_OK)
            elif response_msg == "reject":
                friend_request.delete()
                return Response({"response":"Friend request rejected"}, status=status.HTTP_200_OK)
            else:
                return Response({"response":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response":"Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestList(ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        friend_requests = FriendRequest.objects.filter(receiver=user)
        return friend_requests

class UnFriendView(APIView):
    def post(self, request, user_id):
        user = request.user
        friend = get_object_or_404(User, id=user_id)
        if user not in friend.friends.all():
            return Response({"response":"Not friends with this user"}, status=status.HTTP_400_BAD_REQUEST)
        user.friends.remove(friend)
        return Response({"response":"Unfriended"}, status=status.HTTP_200_OK)




        



