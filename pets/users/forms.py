from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField


User = get_user_model()


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=30, help_text=_('Optional'))
    email = forms.EmailField(max_length=254, help_text=_('Enter a valid email address'))
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user

    class Meta:
        model = User
        fields = ["email", "username", "password"]


class BaseUserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=30, help_text=_('Optional'), empty_value=None, required=False)
    phone_number = PhoneNumberField(empty_value=None, required=False)

    class Meta:
        model = User
        fields = ["username", "phone_number", "image"]


