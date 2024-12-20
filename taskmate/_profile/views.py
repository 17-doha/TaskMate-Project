from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserProfileForm
from signup.models import User
from badge.models import UserBadge, Badge
from task.models import Task
from django.db.models import Q
import base64



# Create your views here.
# def profilepage(request):
#     return render(request, "_profile/profile.html")


# View to display the profile
def profile_view(request):
    user_id = request.session.get('user_id')
    # Get the user profile by ID
    user_profile = get_object_or_404(User, id=user_id) 
    
    completed_tasks_count = Task.objects.filter(
    assigned_to=user_profile, 
    table__label='Done').count()

    all_tasks_count = Task.objects.filter(assigned_to=user_profile).count()
    if(all_tasks_count == 0):
        persentage = 0  
    else:
        persentage = (completed_tasks_count / all_tasks_count) * 100
        
    badges = Badge.objects.filter(num_of_tasks__lte=completed_tasks_count)

    # Update UserBadge table
    for badge in badges:
        UserBadge.objects.get_or_create(user=user_profile, badge=badge)

    # Fetch all earned badges for the user
    earned_badges = UserBadge.objects.filter(user=user_profile).select_related('badge')

    # Prepare data for the template
    badges = [
        {
            'name': ub.badge.badge_name,
            'icon': base64.b64encode(ub.badge.icon).decode('utf-8') if ub.badge.icon else None,
        }
        for ub in earned_badges
    ]
    if(badges == None):
        print("No badges")
        return render(request, '_profile/profile.html', {'user_profile': user_profile,'badges': None,'completed':completed_tasks_count,
        "all":all_tasks_count,"percentage":persentage})

    # Pass the user profile to the template
    return render(request, '_profile/profile.html', {'user_profile': user_profile,'badges': badges,'completed':completed_tasks_count,"all":all_tasks_count,"percentage":persentage})



# View to edit the profile
def profile_edit(request):
    user_id = request.session.get('user_id')
    user_profile = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile) 
        if form.is_valid():
            form.save()  
            return redirect('_profile:profile_view')
        else: 
            print(form.errors) 
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, '_profile/profile.html', {'form': form, 'user_profile': user_profile})


def profile_delete(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id = user_id) 
    user.delete()    
    session = request.session
    session['user_id'] = None
    return redirect('/logout/')
    