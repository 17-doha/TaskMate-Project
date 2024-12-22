from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Notification
from signup.models import User

def fetch_notifications(request):
    user_id = request.session.get('user_id')  # session
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            # Get ALL notifications (both UNREAD and READ)
            notifications = Notification.objects.filter(receiver=user)
            notifications_data = [
                {
                    "id": n.notification_id,
                    "content": n.content,
                    "status": n.status  # "UNREAD" or "READ"
                } 
                for n in notifications
            ]
            return JsonResponse({"notifications": notifications_data}, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)



def mark_read(request, notification_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

        try:
            notification = Notification.objects.get(notification_id=notification_id, receiver_id=user_id)
            #change it in the database that it was read 
            notification.status = "READ"
            notification.save()

            return JsonResponse({"status": "success"})
        except Notification.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Notification does not exist."}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)