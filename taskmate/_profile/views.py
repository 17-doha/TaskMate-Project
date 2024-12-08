from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserProfileForm
from signup.models import User

# Create your views here.
def profilepage(request):
    return render(request, "_profile/profile.html")




# View to display the profile
def profile_view(request):
    # Get the user profile by ID
    user_profile = get_object_or_404(User, id=1) #default for now
    
    # Pass the user profile to the template
    return render(request, '_profile/profile.html', {'user_profile': user_profile})

# View to edit the profile
def profile_edit(request):
    user_profile = User.objects.get(id=1)

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
