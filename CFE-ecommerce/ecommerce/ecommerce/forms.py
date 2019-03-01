from django import forms


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
