from django import forms
from .models import Task
from django.contrib.auth.models import User
from environment.models import Environment

class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task  
        # fields that will be there when editting or creating a task
        fields = ['content', 'status', 'priority', 'deadline', 'assigned_to','start_date']  
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),  
            'start_date': forms.DateInput(attrs={'type': 'date'}),  
        }


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['content', 'status', 'priority', 'assigned_to', 'environment_id', 'deadline', 'start_date']

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Task Description'}))
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    environment_id = forms.ModelChoiceField(queryset=Environment.objects.all(), required=False) 
