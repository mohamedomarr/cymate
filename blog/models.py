from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.utils import timezone
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='blog_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='blog_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    job_title = models.CharField(max_length=100, blank=True)
    job_status = models.CharField(max_length=100, blank=True)
    brief = models.TextField(max_length=300, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    profile_image = models.ImageField(upload_to='profile', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Remove the old signal handlers and add new ones
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if not hasattr(instance, 'user_profile'):
            Profile.objects.create(user=instance)
        instance.user_profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)

# Remove any User.add_to_class calls if they exist


class Post(models.Model):
    POST_TYPES = (
        ('post', 'Post'),
        ('blog', 'Blog'),
        ('question', 'Question'),
        ('event','Event'),
    )
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='post')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trend = models.BooleanField(default=False)
    tags = TaggableManager()  # Using TaggableManager for tagging

    def __str__(self):
        return self.title

    def get_comments_count(self):
        return self.post_comment.count()
    def get_shares_count(self):
        return self.post_share.count()
    def get_reacts_count(self):
        return self.post_react.count()
    def get_saves_count(self):
        return self.post_save.count()


class Save_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_save')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_save')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']  # Prevent duplicate saves


class Reacts(models.Model):
    REACT_TYPES = (
        ('love', 'Love'),
        ('like', 'Like'),
        ('angry', 'Angry'),
        ('sad', 'Sad'),
        ('haha', 'Haha'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_react')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_react')
    react = models.CharField(max_length=10, choices=REACT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']  # One reaction per user per post



class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_share')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_share')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('share', 'Share'),
        ('custom', 'Custom'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='custom')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]

    @classmethod
    def cleanup_old_notifications(cls, days=30):
        """Delete notifications older than specified days"""
        cutoff_date = timezone.now() - datetime.timedelta(days=days)
        cls.objects.filter(created_at__lt=cutoff_date).delete()

    @classmethod
    def create_notification(cls, user, sender, notification_type, post=None):
        message = cls.get_notification_message(sender, notification_type, post)
        return cls.objects.create(
            user=user,
            sender=sender,
            notification_type=notification_type,
            message=message,
            post=post
        )

    @staticmethod
    def get_notification_message(sender, notification_type, post=None):
        messages = {
            'like': f"{sender.username} liked your post",
            'comment': f"{sender.username} commented on your post",
            'share': f"{sender.username} shared your post",
        }
        return messages.get(notification_type, "You have a new notification")

class EmailVerification(models.Model):
    VERIFICATION_TYPES = (
        ('registration', 'Registration'),
        ('password_reset', 'Password Reset'),
    )
    
    email = models.EmailField()
    code = models.CharField(max_length=6)
    verification_type = models.CharField(max_length=20, choices=VERIFICATION_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='email_verifications')
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'code', 'verification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def is_expired(self):
        """Check if the verification code has expired"""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if the verification code is valid (not used and not expired)"""
        return not self.is_used and not self.is_expired()
    
    @classmethod
    def cleanup_expired_codes(cls, hours=24):
        """Delete expired verification codes older than specified hours"""
        cutoff_date = timezone.now() - datetime.timedelta(hours=hours)
        cls.objects.filter(expires_at__lt=cutoff_date).delete()
    
    def __str__(self):
        return f"{self.email} - {self.verification_type} - {self.code}"
