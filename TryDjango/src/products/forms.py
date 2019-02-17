from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price'
        ]


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
