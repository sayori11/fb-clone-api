from .views import *
from django.urls import path, include

urlpatterns = [
    path('users/', UsersListView.as_view()),
    path('user/<int:id>/', UserDetailView.as_view()),
    path('users/activate/<str:uid>/<str:token>/', ActivateUser.as_view()),
    path('friendrequest/<int:user_id>/send/', FriendRequestView.as_view()),
    path('friendrequest/<int:friendrequest_id>/<str:response_msg>/', FriendRequestResponseView.as_view()),
    path('friendrequests/', FriendRequestList.as_view())
]
