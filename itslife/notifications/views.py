from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from .serializers import NotificationSerializer
from .permissions import IsUser
from .models import Notification
from django.db.models import Q

class NotificationViewSet(mixins.RetrieveModelMixin, 
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsUser]
    http_method_names = ['get', 'head', 'delete']

    def get_queryset(self):
        user = self.request.user
        notifications = Notification.objects.filter(to_user=user, user_has_seen=False)
        return notifications

class NotificationSeenView(APIView):

    def post(self, request, notif_id, format=None):
        notif = Notification.objects.get(id=notif_id)
        notif.user_has_seen = True
        notif.save()
        return Response({"response":"Notification seen"})
