from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={"placeholder": "Enter your title"}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            "placeholder": "Enter your description",
            "class": "my-description-class",
            "rows": 10,
            "cols": 20,
            "id": "my-description-id",
        }))
    price = forms.DecimalField(initial=1.99)

    # New form field
    email = forms.EmailField()

    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price', 'email'
        ]

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if "Chain" not in title:
            raise forms.ValidationError("This is not a proper title")

        return title

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if not email.endswith("edu"):
            raise forms.ValidationError("Enter a valid email(ending with edu)")

        return email


# This is a pure Django form
class RawProductForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder" : "Enter your title"}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            "placeholder":"Enter your description",
            "class": "my-description-class",
            "rows": 10,
            "cols": 20,
            "id": "my-description-id",
    }))
    price = forms.DecimalField(initial=1.99)
