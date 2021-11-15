from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import NotificationSerializer
from .permissions import IsUser
from .models import Notification

class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        user = self.request.user
        notifications = Notification.objects.filter(to_user=user)
        return notifications
