from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from signup.models import User
from environment.models import Environment
from .models import Invitation
from Notification.models import Notification

def create_invitation(request):
    if request.method == "POST":
        email = request.POST.get("email")
        environment_label = request.POST.get("environment_label")

        if not email or not environment_label:
            return JsonResponse({"status": "error", "message": "email and environment are required"})

        sender_email = request.session.get('user_email')
        sender_user = User.objects.get(email=sender_email)

        receiver = get_object_or_404(User, email=email)
        environment = get_object_or_404(Environment, label=environment_label)

        if environment.admin != sender_user:
            return JsonResponse({"status": "error", "message": "You don't have access to this environment"})

        Invitation.objects.create(
            sender=sender_user,
            receiver=receiver,
            environment=environment,
            invitation_status="PENDING"
        )
        
        Notification.objects.create(
            content=f"{sender_user.email} has invited you to join {environment.label}.",
            receiver=receiver,
            status="UNREAD"
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{receiver.id}", 
            {
                "type": "send_notification",
                "message": f"You have a new environment invitation for {environment.label}!"
            }
        )

        print(f"Notification sent to group: user_{receiver.id}")
        return JsonResponse({
            "status": "success",
            "message": "Invitation has been sent successfully!",
            "receiver_id": receiver.id  # Include receiver_id in the response
        })

    return JsonResponse({"status": "error", "message": "Invalid request"})
