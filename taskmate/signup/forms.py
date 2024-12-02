from django import  forms
from .models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    """
    A form for user sign-up that extends Django's ModelForm.

    This form is used to collect user information during the sign-up process.
    It includes fields for first name, last name, email, and password. The form
    performs validation to ensure that the email is unique and that the password
    meets certain criteria.

    Attributes:
        Meta (class): A nested class that specifies the model and fields to be used
                      in the form.

    Methods:
        clean_email(): Validates that the provided email is not already in use.
                       Raises a ValidationError if the email is taken.
        
        clean_password(): Validates the password to ensure it is at least 8 characters
                          long and contains both letters and numbers. Raises a 
                          ValidationError if these conditions are not met.
    """

    class Meta:
        model = User
        # Add fields we will be collecting info for
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email not available for use")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Check password length
        if len(password) < 8:
            raise ValidationError("Password can't be less than 8 characters")
        # Check for number and letters in password
        if password.isalpha() or password.isnumeric():
            raise ValidationError("Password should contain both letters and numbers")

        return password