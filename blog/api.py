from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Notification, Post, Save_Post, Reacts, Share, Comment, Profile, User
from .serializer import NotificationSerializer, PostListSerializer, ProfileSerializer, CommentSerializer
from .mixins import NotificationMixin
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostInteractionViewSet(NotificationMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def retrieve(self, request, pk=None):
        """Handle GET requests"""
        try:
            post = Post.objects.get(id=pk)
            serializer = PostListSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def interact(self, request, pk=None):
        """Handle post interactions (react, share, save)"""
        try:
            action_type = request.data.get('action_type')
            react_type = request.data.get('react_type')

            post = Post.objects.get(id=pk)
            user = request.user

            if action_type == 'react' and react_type:
                return self._handle_react(user, post, react_type)
            elif action_type == 'share':
                return self._handle_share(user, post)
            elif action_type == 'save':
                return self._handle_save(user, post)
            else:
                return Response(
                    {'error': 'Invalid action type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """Handle post comments"""
        try:
            content = request.data.get('content')

            if not content:
                return Response(
                    {'error': 'Comment content is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            post = Post.objects.get(id=pk)
            comment = Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )

            return Response(
                CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED
            )
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def _handle_react(self, user, post, react_type):
        try:
            if react_type not in ['like', 'love', 'haha', 'wow', 'sad', 'angry']:
                return Response(
                    {'error': 'Invalid reaction type'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            react, created = Reacts.objects.get_or_create(
                user=user,
                post=post,
                defaults={'react': react_type}
            )
            if not created:
                if react.react == react_type:
                    react.delete()
                else:
                    react.react = react_type
                    react.save()
            return Response(
                PostListSerializer(post, context={'request': self.request}).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _handle_share(self, user, post):
        share, created = Share.objects.get_or_create(user=user, post=post)
        if not created:
            share.delete()
        return Response(
            PostListSerializer(post, context={'request': self.request}).data,
            status=status.HTTP_200_OK
        )

    def _handle_save(self, user, post):
        save, created = Save_Post.objects.get_or_create(user=user, post=post)
        if not created:
            save.delete()
        return Response(
            PostListSerializer(post, context={'request': self.request}).data,
            status=status.HTTP_200_OK
        )

class PostListApi(NotificationMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = PostListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Return all posts
        return Post.objects.all()\
            .select_related('author')\
            .prefetch_related('post_comment', 'post_react', 'post_share', 'post_save')\
            .order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if not isinstance(response.data, dict):
            response.data = {
                'posts': response.data
            }
        return response

class PostDetailApi(NotificationMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = PostListSerializer

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
            serializer = PostListSerializer(post, context={'request': request})
            return Response({
                'post': serializer.data
            })
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class PostSavedListApi(NotificationMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = PostListSerializer

    def list(self, request):
        user = request.user
        try:
            if hasattr(user, 'user_save'):
                saved_posts = user.user_save.all()
                posts = Post.objects.filter(post_save__in=saved_posts).order_by('-created_at')
                serializer = PostListSerializer(posts, many=True, context={'request': request})
                return Response({
                    'saved_posts': serializer.data
                })
            else:
                return Response({
                    'saved_posts': []
                })
        except Exception as e:
            return Response({
                'error': str(e),
                'saved_posts': []
            })

class ProfileListApi(NotificationMixin, APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            profile = user.user_profile

            # Serialize profile data
            profile_serializer = ProfileSerializer(profile)

            # Get user posts
            user_posts = Post.objects.filter(author=user).order_by('-created_at')
            posts_data = PostListSerializer(
                user_posts,
                many=True,
                context={'request': request}
            ).data

            # Combine all data
            response_data = profile_serializer.data
            response_data.update({
                'posts': posts_data,
            })

            return Response(response_data)

        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )

# Add NotificationMixin to all your other API views

class NotificationAPI(NotificationMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = NotificationSerializer

    def list(self, request):
        """Get all unread notifications for current user"""
        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark specific notification as read"""
        try:
            notification = Notification.objects.select_for_update().get(
                id=pk,
                user=request.user
            )
            notification.delete()
            return Response(status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).select_for_update().delete()
        return Response(status=status.HTTP_200_OK)

class CreateProfileApi(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Check if profile already exists
            if hasattr(request.user, 'user_profile'):
                return Response(
                    {'error': 'Profile already exists for this user'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create profile data dictionary
            profile_data = {
                'job_title': request.data.get('job_title', ''),
                'job_status': request.data.get('job_status', ''),
                'brief': request.data.get('brief', ''),
                'years_of_experience': request.data.get('years_of_experience', 0),
                'phone_number': request.data.get('phone_number', ''),
            }

            # Handle profile image if provided
            if 'profile_image' in request.FILES:
                profile_data['profile_image'] = request.FILES['profile_image']

            # Create profile
            profile = Profile.objects.create(
                user=request.user,
                **profile_data
            )

            # Serialize and return the created profile
            serializer = ProfileSerializer(profile)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class EditProfileApi(NotificationMixin, APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            # Check if profile exists
            if not hasattr(request.user, 'user_profile'):
                return Response(
                    {'error': 'Profile does not exist for this user'},
                    status=status.HTTP_404_NOT_FOUND
                )

            profile = request.user.user_profile

            # Update profile data
            if 'job_title' in request.data:
                profile.job_title = request.data['job_title']
            if 'job_status' in request.data:
                profile.job_status = request.data['job_status']
            if 'brief' in request.data:
                profile.brief = request.data['brief']
            if 'years_of_experience' in request.data:
                profile.years_of_experience = request.data['years_of_experience']
            if 'phone_number' in request.data:
                profile.phone_number = request.data['phone_number']

            # Handle profile image update
            if 'profile_image' in request.FILES:
                # Delete old image if it exists
                if profile.profile_image:
                    profile.profile_image.delete()
                profile.profile_image = request.FILES['profile_image']

            # Save the updated profile
            profile.save()

            # Return the updated profile data
            serializer = ProfileSerializer(profile)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

class PostEditApi(NotificationMixin, APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    def get_post(self, post_id, user):
        try:
            # Get post and verify ownership
            return Post.objects.get(id=post_id, author=user)
        except Post.DoesNotExist:
            return None

    def put(self, request, post_id, *args, **kwargs):
        post = self.get_post(post_id, request.user)
        if not post:
            return Response(
                {'error': 'Post not found or you do not have permission to edit this post'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Update post data
            if 'title' in request.data:
                post.title = request.data['title']
            if 'content' in request.data:
                post.content = request.data['content']
            if 'post_type' in request.data:
                post.post_type = request.data['post_type']

            # Handle image update
            if 'image' in request.FILES:
                # Delete old image if it exists
                if post.image:
                    post.image.delete()
                post.image = request.FILES['image']

            # Handle tags if provided
            # if 'tags' in request.data:
            #     post.tags.clear()  # Remove existing tags
            #     tags = request.data.get('tags', '').split(',')  # Expecting comma-separated tags
            #     post.tags.add(*[tag.strip() for tag in tags if tag.strip()])
            if 'tags' in request.data:
                post.tags.clear()  # Remove existing tags
                tags_value = request.data.get('tags', '')
                if isinstance(tags_value, list):
                    tags = tags_value
                elif isinstance(tags_value, str):
                    tags = [tag.strip() for tag in tags_value.split(',') if tag.strip()]
                else:
                    tags = []
                post.tags.add(*tags)

            # Save the updated post
            post.save()

            # Return the updated post data
            serializer = PostListSerializer(post, context={'request': request})
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, post_id, *args, **kwargs):
        return self.put(request, post_id, *args, **kwargs)

    def delete(self, request, post_id, *args, **kwargs):
        post = self.get_post(post_id, request.user)
        if not post:
            return Response(
                {'error': 'Post not found or you do not have permission to delete this post'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Delete the image if it exists
            if post.image:
                post.image.delete()

            # Delete the post
            post.delete()

            return Response(
                {'message': 'Post deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
