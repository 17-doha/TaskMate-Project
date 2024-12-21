from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Invitation
from .forms import InvitationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail  # For email invitations
from django.conf import settings  # For email configurations

@login_required
def invite_participants(request):
    shareable_link = request.build_absolute_uri('/shared-environment/')  # Compute the link in the view

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.invited_by = request.user
            invitation.link = shareable_link
            invitation.save()
            messages.success(request, f"Invitation successfully sent to {invitation.email}!")
            return redirect(reverse('invite_participants'))
    else:
        form = InvitationForm()
    
    return render(request, 'invitations/invite_participants.html', {
        'form': form,
        'shareable_link': shareable_link,  # Pass the link to the template
    })

@login_required
def send_invitation(request, environment_id):
    """
    Purpose:
        Handles sending invitations to users to join an environment.

    Input:
        - HTTP Method: POST
        - Path Parameter:
            - environment_id: The ID of the environment for which the invitation is being sent.
        - JSON Body:
            - email: The email of the user to invite.
            - access_type: The type of accessibility to grant (Participant, subadmin, Admin).

    Output:
        - JSON Response:
            - Success: {'status': 'success', 'message': 'Invitation sent successfully.'}
            - Error: {'status': 'error', 'message': 'Error message.'}

    Logic:
        1. Parse the email and access type from the request body.
        2. Verify the environment exists and that the user is authorized to send invitations.
        3. Check if the invited user already has access to the environment.
        4. Create or update the `UserCanAccess` entry for the invited user.
        5. Send an invitation email (if configured).
        6. Return a success or error response.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        access_type = data.get('access_type', 'Participant')  # Default to 'Participant'

        # Get the environment and verify the user is the admin
        environment = get_object_or_404(Environment, environment_id=environment_id, admin=request.user)

        # Ensure the invited user exists
        try:
            invited_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist.'})

        # Check if the user already has access
        user_access, created = UserCanAccess.objects.get_or_create(
            user=invited_user,
            environment=environment,
            defaults={'type_of_accessibility': access_type, 'invitation_status': 'Pending'}
        )
        if not created:
            return JsonResponse({'status': 'error', 'message': 'User already has access or an invitation is pending.'})

        # Send an email notification (if email settings are configured)
        send_mail(
            subject=f"Invitation to Join Environment: {environment.label}",
            message=f"You have been invited to join the environment '{environment.label}' as {access_type}. Please log in to accept the invitation.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return JsonResponse({'status': 'success', 'message': 'Invitation sent successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})