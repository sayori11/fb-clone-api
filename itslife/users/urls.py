from .views import UsersListView, UserDetailView, ActivateUser
from django.urls import path, include


urlpatterns = [
    path('users/', UsersListView.as_view()),
    path('user/<id>/', UserDetailView.as_view()),
    path('users/activate/<str:uid>/<str:token>/', ActivateUser.as_view())
]