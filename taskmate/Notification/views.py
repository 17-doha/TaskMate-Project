from django.http import JsonResponse
from .models import Notification
from signup.models import User

def fetch_notifications(request):
    user_id = request.session.get('user_id')   #using session bta3 doha

    if user_id: #lw ah f hwa keda authenticated
        try:
            user = User.objects.get(id=user_id) 
            notifications = Notification.objects.filter(receiver=user, status="UNREAD")  #b geed kol el unread notifications
            notifications_data = [
                {"id": n.notification_id, "content": n.content, "status": n.status} for n in notifications
            ]
            return JsonResponse({"notifications": notifications_data}, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found "}, status=404)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)
