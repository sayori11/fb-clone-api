from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostsViewset, UserPostsViewset, CommentsListViewSet, CommentsDetailViewSet, RepliesListViewSet, RepliesDetailViewSet


router = DefaultRouter()
router.register('', PostsViewset, basename='posts')

user_posts = UserPostsViewset.as_view({
    'get':'list'
})

comments_list = CommentsListViewSet.as_view()
comments_detail = CommentsDetailViewSet.as_view()
replies_list = RepliesListViewSet.as_view()
replies_detail = RepliesDetailViewSet.as_view()

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:user_id>/', user_posts, name='user_posts'),
    path('<int:post_id>/comments/', comments_list, name='comments_list'),
    path('<int:post_id>/comments/<int:pk>/', comments_detail, name='comments_detail'),
    path('comments/<int:comment_id>/replies/', replies_list, name='replies_list'),
    path('comments/<int:comment_id>/replies/<int:pk>/', replies_detail, name='replies_detail')
]

