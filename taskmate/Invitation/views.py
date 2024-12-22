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
        #bta5od el values mn el pop up bta3 el invitation 
        email = request.POST.get("email")
        environment_label = request.POST.get("environment_label")

        if not email or not environment_label:
            return JsonResponse({"status": "error", "message": "email and environment both are required"})

        sender_email = request.session.get('user_email')
        sender_user = User.objects.get(email=sender_email)

        receiver = get_object_or_404(User, email=email)
        environment = get_object_or_404(Environment, label=environment_label)
  #check if user sender admin of this environment or not
        if environment.admin != sender_user:
            return JsonResponse({"status": "error", "message": "You don't have access to this environment"})
          # add new invitation record 
        Invitation.objects.create(
            sender=sender_user,
            receiver=receiver,
            environment=environment,
            invitation_status="PENDING"
        )
            #add new notification record
        Notification.objects.create(
            content=f"{sender_user.email} has invited you to join {environment.label}.",
            receiver=receiver,
            status="UNREAD"
        )
        #bt3mel layer feha el user elle howa el reciever we group name reciever.id
        channel_layer = get_channel_layer()

        #async to sync ( the create_invitation is sync but websockets async so async_to_sync make async code is callable via sync code)
        async_to_sync(channel_layer.group_send)(
            f"user_{receiver.id}", 
            {
                "type": "send_notification",
                "message": f"You have a new environment invitation for {environment.label}!"
            }
        )
        #return these json response for index.html w hnak b y route for link in notification/routing.py elly feh by3mel websocket connection
        print(f"Notification sent to group: user_{receiver.id}")
        return JsonResponse({
            "status": "success",
            "message": "Invitation has been sent successfully!",
            "receiver_id": receiver.id  # Include receiver_id in the response
        })

    return JsonResponse({"status": "error", "message": "Invalid request"})
