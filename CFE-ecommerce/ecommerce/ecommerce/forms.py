from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    """
    Class that inherits from the Django's internal forms.Form class
    """
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                             "id": "form_full_name",
                                                             "placeholder": "Your Full Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control",
                                                            "placeholder": "Your Email"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",
                                                           "placeholder": "Your message"}))

    # Error handling mechanism
    # def clean_<field_name>

    def clean_email(self):
        """
        CError handling mechanism for email
        :return:
        """
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gamil.com")

        return email


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


