from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from .permissions import IsUserOrReadOnly
import requests
from rest_framework.response import Response

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


