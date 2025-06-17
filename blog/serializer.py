from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from .models import User, Profile, Post, Save_Post, Reacts, Share, Comment, Notification
from taggit.serializers import TagListSerializerField, TaggitSerializer

class CustomRegisterSerializer(RegisterSerializer):
    # Add custom fields for registration
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        })
        return data

class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    posts_count = serializers.SerializerMethodField()
    profile_picture = serializers.ImageField(source='profile_image', required=False)  # Alias for API consistency

    class Meta:
        model = Profile
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'job_title',
            'job_status',
            'brief',
            'years_of_experience',
            'profile_image',
            'profile_picture',  # Alias field
            'phone_number',
            'posts_count'
        ]

    def get_posts_count(self, obj):
        return obj.user.user_posts.count()
    
    def validate_profile_image(self, value):
        """Validate profile image upload"""
        if value:
            # Check file size (max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if value.size > max_size:
                raise serializers.ValidationError("Profile image size cannot exceed 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Only JPEG, PNG and GIF image formats are allowed."
                )
        
        return value
    
    def validate_profile_picture(self, value):
        """Validate profile picture upload (alias for profile_image)"""
        return self.validate_profile_image(value)

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'sender', 'notification_type', 'message', 'is_read', 'created_at']
        read_only_fields = ['created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['created_at']

class PostListSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = TagListSerializerField()
    comments_count = serializers.SerializerMethodField()
    shares_count = serializers.SerializerMethodField()
    reacts_count = serializers.SerializerMethodField()
    saves_count = serializers.SerializerMethodField()
    comments = CommentSerializer(source='post_comment', many=True, read_only=True)
    # Add new fields for interaction status
    user_reaction = serializers.SerializerMethodField()
    is_shared = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'post_type',
            'title',
            'content',
            'image',
            'tags',
            'created_at',
            'trend',
            'comments_count',
            'shares_count',
            'reacts_count',
            'saves_count',
            'comments',
            'user_reaction',
            'is_shared',
            'is_saved'
        ]
        read_only_fields = ['created_at', 'trend']

    def get_comments_count(self, obj):
        return obj.get_comments_count()

    def get_shares_count(self, obj):
        return obj.get_shares_count()

    def get_reacts_count(self, obj):
        return obj.get_reacts_count()

    def get_saves_count(self, obj):
        return obj.get_saves_count()

    def get_user_reaction(self, obj):
        user = self.context.get('request').user
        try:
            reaction = obj.post_react.get(user=user)
            return reaction.react
        except Reacts.DoesNotExist:
            return None

    def get_is_shared(self, obj):
        user = self.context.get('request').user
        return obj.post_share.filter(user=user).exists()

    def get_is_saved(self, obj):
        user = self.context.get('request').user
        return obj.post_save.filter(user=user).exists()

class ReactSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Reacts
        fields = ['id', 'user', 'post', 'react', 'created_at']
        read_only_fields = ['created_at']

class ShareSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Share
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['created_at']

class SavePostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Save_Post
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['created_at']

class CreateProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile_image', required=False)  # Alias for API consistency
    
    class Meta:
        model = Profile
        fields = [
            'job_title',
            'job_status',
            'brief',
            'years_of_experience',
            'profile_image',
            'profile_picture',  # Alias field
            'phone_number',
        ]
    
    def validate_profile_image(self, value):
        """Validate profile image upload"""
        if value:
            # Check file size (max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if value.size > max_size:
                raise serializers.ValidationError("Profile image size cannot exceed 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Only JPEG, PNG and GIF image formats are allowed."
                )
        
        return value
    
    def validate_profile_picture(self, value):
        """Validate profile picture upload (alias for profile_image)"""
        return self.validate_profile_image(value)

