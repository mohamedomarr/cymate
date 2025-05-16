from django.urls import path
from .api import (
    PostListApi,
    PostInteractionViewSet,
    PostDetailApi,
    PostSavedListApi,
    ProfileListApi,
    NotificationAPI,
    CreateProfileApi,
    EditProfileApi,
    PostEditApi
)

urlpatterns = [
    # Post related endpoints
    path('posts/', PostListApi.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailApi.as_view({'get': 'retrieve'}), name='post-detail'),
    path('posts/<int:pk>/interact/', PostInteractionViewSet.as_view({
        'post': 'interact',
        'get': 'retrieve'
    }), name='post-interact'),
    path('posts/<int:pk>/comment/', PostInteractionViewSet.as_view({
        'post': 'comment'
    }), name='post-comment'),
    path('posts/saved/', PostSavedListApi.as_view({'get': 'list'}), name='saved-posts'),
    path('posts/<int:post_id>/edit/', PostEditApi.as_view(), name='post-edit'),

    # Profile related endpoints
    path('profile/<str:username>/', ProfileListApi.as_view(), name='profile-detail'),
    path('profile/create/', CreateProfileApi.as_view(), name='profile-create'),
    path('profile/edit/', EditProfileApi.as_view(), name='profile-edit'),

    # Notification endpoints
    path('notifications/', NotificationAPI.as_view({'get': 'list'}), name='notifications'),
    path('notifications/<int:pk>/mark-read/', NotificationAPI.as_view({'post': 'mark_read'}), name='mark-notification-read'),
    path('notifications/mark-all-read/', NotificationAPI.as_view({'post': 'mark_all_read'}), name='mark-all-notifications-read'),
]
