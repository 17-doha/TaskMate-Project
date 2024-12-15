from django.http import JsonResponse
from Notification.models import Notification

def get_notifications(request):
    if request.user.is_authenticated:
        # Fetch unread notifications for the logged-in user
        notifications = Notification.objects.filter(receiver=request.user, status="UNREAD")
        data = {
            "notifications": [{"message": n.content} for n in notifications]
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)
