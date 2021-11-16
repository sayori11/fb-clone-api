from .views import NotificationViewSet, NotificationSeenView
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:notif_id>/seen/', NotificationSeenView.as_view(), name='notification_seen'),
]