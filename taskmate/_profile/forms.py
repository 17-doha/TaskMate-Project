from django import forms
from signup.models import User
from django.core.validators import RegexValidator

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','phone_number','age']

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(
        required=True,
        validators=[RegexValidator(r'^\d+$', 'Phone number must be numeric.')], 
        max_length=15  
    )
    
    age = forms.CharField(
        required=False,
        validators=[RegexValidator(r'^\d+$', 'Age must be a valid number')]
    )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age:
            try:
                age = int(age)  
                if age <= 0: 
                    raise ValidationError("Age must be a positive number.")
            except ValueError:
                raise ValidationError("Age must be a valid number.")
        return age
    