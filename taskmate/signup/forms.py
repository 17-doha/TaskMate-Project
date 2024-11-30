from django import  forms
from .models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        #Add fields we will be collecting info for
        fields = ['first_name','last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise ValidationError("Email not available for use")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        #check password length
        if len(password) < 8:
            raise ValidationError("Password can't be less than 8 characters")
        #check for number and letters is password
        if password.isalpha() or password.isnumeric():
            raise ValidationError("Password should contains both letters and numbers")

        return password
