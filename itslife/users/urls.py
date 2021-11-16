from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UsersDetailView, basename='users')

urlpatterns = [
    # path('users/', UsersListView.as_view(), name='users_list'),
    # path('users/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('', include(router.urls)),
    path('users/activate/<str:uid>/<str:token>/', ActivateUser.as_view(), name='activate_user'),
    path('friendrequest/<int:user_id>/send/', FriendRequestView.as_view(), name='friend_request_send'),
    path('friendrequest/<int:friendrequest_id>/<str:response_msg>/', FriendRequestResponseView.as_view(), name='friend_request_respond'),
    path('friendrequests/', FriendRequestList.as_view(), name='friend_requests_list'),
    path('unfriend/<int:user_id>/', UnFriendView.as_view(), name='unfriend')
]
