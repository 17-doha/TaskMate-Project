from django import forms
from .models import Badge

class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['badge_name', 'num_of_tasks', 'icon']  



