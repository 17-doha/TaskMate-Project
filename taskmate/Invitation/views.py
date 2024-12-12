from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from signup.models import User
from environment.models import Environment
from .models import Invitation # Import your models
from Notification.models import Notification
# from django.contrib.auth.decorators import login_required   //lama el sessions tt3emel

def share_page(request):
    return render(request, "Invitation/share.html")

def create_invitation(request):
    if request.method == "POST":
        # Get email and environment label from the POST request
        email = request.POST.get("email")
        environment_label = request.POST.get("environment_label")

        # Ensure both fields are provided
        if not email or not environment_label:
            return JsonResponse({"status": "error", "message": "Both email and environment name are required."})

        # Get the sender as the currently logged-in user
        # sender = request.user   # lama el sessions tt3emel bardo hwa bygbha 3la tool (logged in user)
        sender = get_object_or_404(User, email="sarahsleem7@gmail.com") 
        # Validate that the sender is authenticated
        if not sender.is_authenticated:
            return JsonResponse({"status": "error", "message": "You must be logged in to send an invitation."})

        # Get the receiver and environment
        receiver = get_object_or_404(User, email=email)  # Get the invited user by email
        environment = get_object_or_404(Environment, label=environment_label)  # Get the environment by its label

        # Create invitation record
        invitation = Invitation.objects.create(
            sender=sender,
            receiver=receiver,
            environment=environment,
            invitation_status="PENDING"
        )

        # Create notification record
        notification = Notification.objects.create(
            content=f"{sender.username} has invited you to join the {environment.label} environment.",
            receiver=receiver,
            status="UNREAD"
        )

        # Send notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{receiver.id}",  # Group name for the invited user
            {
                "type": "send_notification",
                "message": notification.content,
            }
        )

        return JsonResponse({"status": "success", "message": "Invitation sent successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request"})
