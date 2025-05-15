from django.urls import path
from .api import PostListApi, PostInteractionViewSet

urlpatterns = [
    path('posts/', PostListApi.as_view(), name='post-list'),
    path('posts/<int:pk>/interact/', PostInteractionViewSet.as_view({
        'post': 'interact',
        'get': 'retrieve'
    }), name='post-interact'),
    path('posts/<int:pk>/comment/', PostInteractionViewSet.as_view({
        'post': 'comment'
    }), name='post-comment'),
    # ... other URLs
]

