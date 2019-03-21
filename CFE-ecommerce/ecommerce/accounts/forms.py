from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    """
    Class based form for user to log-in into
    """
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    """
    Class based form for registering a user
    """
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    email = forms.EmailField()

    # Both the password and confirm password should work together
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password_2 = self.cleaned_data.get("password_2")

        if password != password_2:
            raise forms.ValidationError("Passwords should match")

        return data

    def clean_user_name(self):
        """
        Check if a user already exists.
        To solve the UNIQUE constraint error
        :return:
        """
        user_name = self.cleaned_data.get("user_name")

        # Query Set
        qs = User.objects.filter(username=user_name)
        if qs.exists():
            raise forms.ValidationError("User name is taken")
        return user_name

    def clean_email(self):
        """
        Check if a user already exists.
        To solve the UNIQUE constraint error
        :return:
        """
        email = self.cleaned_data.get("email")
        print("The email is", email)
        # Query Set
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken")
        return email