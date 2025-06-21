from rest_framework.response import Response
from .models import Notification, User
from .serializer import NotificationSerializer  # Updated import

class NotificationMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if request.user.is_authenticated and response.status_code < 400:
            try:
                # Get unread notifications
                if isinstance(request.user, User):
                    notifications = Notification.objects.filter(
                        user=request.user,
                        is_read=False
                    ).select_related('sender', 'sender__user_profile', 'post').order_by('-created_at')

                    # Serialize notifications with request context
                    notification_data = NotificationSerializer(
                        notifications, 
                        many=True, 
                        context={'request': request}
                    ).data

                    # Handle different response data types
                    if not hasattr(response, 'data'):
                        response.data = {}

                    if not isinstance(response.data, dict):
                        response.data = {
                            'results': response.data,
                            'notifications': notification_data,
                            'unread_notifications_count': notifications.count()
                        }
                    else:
                        response.data['notifications'] = notification_data
                        response.data['unread_notifications_count'] = notifications.count()
            except Exception as e:
                # Just log the error and continue
                print(f"Error in NotificationMixin: {str(e)}")

        return super().finalize_response(request, response, *args, **kwargs)

