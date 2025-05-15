from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Reacts, Comment, Share, User, Notification

@receiver(post_save, sender=Reacts)
def create_react_notification(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.user:
        Notification.create_notification(
            user=instance.post.author,
            sender=instance.user,
            notification_type='like',
            post=instance.post
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.user:
        Notification.create_notification(
            user=instance.post.author,
            sender=instance.user,
            notification_type='comment',
            post=instance.post
        )

@receiver(post_save, sender=Share)
def create_share_notification(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.user:
        Notification.create_notification(
            user=instance.post.author,
            sender=instance.user,
            notification_type='share',
            post=instance.post
        )

@receiver(m2m_changed, sender=User.follow.through)
def create_follow_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            followed_user = User.objects.get(id=user_id)
            Notification.create_notification(
                user=followed_user,
                sender=instance,
                notification_type='follow'
            )