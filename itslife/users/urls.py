from .views import UsersListView, UserDetailView, ActivateUser, FriendRequestView, FriendRequestResponseView, FriendRequestList
from django.urls import path, include

urlpatterns = [
    path('users/', UsersListView.as_view()),
    path('user/<int:id>/', UserDetailView.as_view()),
    path('users/activate/<str:uid>/<str:token>/', ActivateUser.as_view()),
    path('friendrequest/send/<int:user_id>/', FriendRequestView.as_view()),
    path('friendrequest/<int:user_id>/<str:response_msg>/', FriendRequestResponseView.as_view()),
    path('friendrequests/', FriendRequestList.as_view())
]
