import io
import sys

from PIL import Image
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
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
    crop_data = forms.JSONField(
        required=False)  # expected data: { x_offset: float, y_offset: float, width: float, height: float }

    class Meta:
        model = User
        fields = ["username", "phone_number", "image", "crop_data"]

    def clean(self):
        cleaned_data = super().clean()
        crop_data = cleaned_data.get("crop_data")

        required_keys = {"x_offset", "y_offset", "width", "height"}
        if not crop_data or not required_keys.issubset(crop_data.keys()):
            crop_data["image"] = None

        return cleaned_data

    def save(self, commit=True):
        original_image = self.cleaned_data["image"]

        if original_image is not None:
            crop_data = self.cleaned_data["crop_data"]
            pil_image = Image.open(original_image)
            pil_image = pil_image.crop(
                (crop_data["x_offset"],
                 crop_data["y_offset"],
                 crop_data["x_offset"] + crop_data["width"],
                 crop_data["y_offset"] + crop_data["height"],)
            )

            buffer = io.BytesIO()
            pil_image.save(buffer, format=original_image.image.format)
            self.instance.image = InMemoryUploadedFile(
                buffer, "ImageField", original_image.name, original_image.content_type, sys.getsizeof(buffer), None)

        super(BaseUserEditForm, self).save(commit)
