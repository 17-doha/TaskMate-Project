from django import forms
from signup.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    
