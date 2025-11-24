from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": f"Enter {name.replace('_', ' ')}"
            })

        for name, field in self.fields.items():
            if self.errors.get(name):
                existing_classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = existing_classes + " is-invalid"
