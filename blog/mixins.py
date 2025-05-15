from rest_framework.response import Response
from .models import Notification
from .serializer import NotificationSerializer  # Updated import

class NotificationMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if request.user.is_authenticated and response.status_code < 400:
            # Get unread notifications
            notifications = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).order_by('-created_at')
            
            # Serialize notifications
            notification_data = NotificationSerializer(notifications, many=True).data
            
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
        
        return super().finalize_response(request, response, *args, **kwargs)

