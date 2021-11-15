from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, FriendRequestSerializer
from .models import User, FriendRequest
from notifications.models import Notification
from .permissions import IsUserOrReadOnly
import requests


class UsersListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

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
            return Response({'detail': 'Activated successfully!'})
        else:
            return Response(response.json())

class FriendRequestView(APIView):

    def post(self, request, user_id, format = None):
        sender = request.user
        receiver = User.objects.get(id=user_id)
        fr = FriendRequest.objects.create(sender=sender, receiver=receiver)
        Notification.objects.create(notification_type='friend_request', from_user=sender, to_user=receiver, friend_request= fr)
        return Response({"response":"Friend request sent successfully!"}, status=status.HTTP_202_ACCEPTED)

class FriendRequestResponseView(APIView):

    def post(self, request, friendrequest_id, response_msg, format = None):
        friend_request = FriendRequest.objects.get(id=friendrequest_id)
        sender = friend_request.sender
        receiver = friend_request.receiver
        if request.user == receiver:
            if response_msg == "accept":
                friend_request.receiver.friends.add(sender)
                friend_request.delete()
                Notification.objects.create(notification_type='friend_request_accept', from_user=receiver, to_user=sender)
                return Response({"response":"Friend request accepted"})
            elif response_msg == "reject":
                friend_request.delete()
                return Response({"response":"Friend request deleted"})
            else:
                return Response({"response":"Invalid request"})
        else:
            return Response({"response":"Invalid user"})

class FriendRequestList(ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        friend_requests = FriendRequest.objects.filter(receiver=user)
        return friend_requests





        



