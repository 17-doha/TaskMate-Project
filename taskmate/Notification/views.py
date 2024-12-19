from django.http import JsonResponse
from .models import Notification
from signup.models import User

def fetch_notifications(request):
    """
    Fetches notifications for the user based on the session user_id.

    Logic:
    - If the user_id is present in the session, retrieves unread notifications for that user.
    - If no user_id is in the session, returns an error indicating the user is not authenticated.

    Inputs:
    - request: HttpRequest object.

    Outputs:
    - JSON response containing notifications for authenticated users.
    - Error JSON response for unauthenticated users.
    """
    user_id = request.session.get('user_id')  # Get user_id from the session

    if user_id:  # Check if the user is authenticated
        try:
            user = User.objects.get(id=user_id)  # Retrieve the user object
            notifications = Notification.objects.filter(receiver=user, status="UNREAD")
            notifications_data = [
                {"id": n.notification_id, "content": n.content, "status": n.status} for n in notifications
            ]
            return JsonResponse({"notifications": notifications_data}, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)
