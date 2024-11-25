from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task  
        fields = ['content', 'status', 'priority', 'deadline', 'assigned']  
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),  
        }