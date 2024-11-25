from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task  
        # fields that will be there when editting or creating a task
        fields = ['content', 'status', 'priority', 'deadline', 'assigned']  
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),  
        }