from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import ThumbnailModel
from core.utils import get_storage_path, select_storage

from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(UserManager):
    def _create_user(self, email, password=None, username=None, **extra_fields):
        if username:
            username = User.normalize_username(username)
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.

        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("type", [User.Types.ADMIN])

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username=username, email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, ThumbnailModel):
    class Types(models.IntegerChoices):
        ADMIN = (0, "Administrator")
        COMMON = (1, "Common user")
        MODERATOR = (2, "Moderator")

    base_type = Types.COMMON

    email = models.EmailField(_("Email"), blank=False, null=False, unique=True)
    type = models.IntegerField(_("Type"), choices=Types.choices)

    username = models.CharField(_("Username"), blank=False, null=True, unique=True, max_length=30)
    phone_number = PhoneNumberField(_("Phone number"), blank=False, null=True, default=None, max_length=20)
    image = models.ImageField(upload_to=get_storage_path, blank=True, null=False, storage=select_storage)
    image_preview = models.ImageField(upload_to=get_storage_path, blank=True, null=False, storage=select_storage)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type

        self._make_thumbnail("image", "image_preview")
        return super(User, self).save(*args, **kwargs)

    def get_image(self):
        return self._get_image(field_name="image", default=f"{settings.STATIC_URL}assets/images/User_photo.jpg")

    def get_image_preview(self):
        return self._get_image(field_name="image_preview", default=f"{settings.STATIC_URL}assets/images/User_photo.jpg")


class RegularUserManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COMMON)


class CommonUser(User):
    base_type = User.Types.COMMON

    objects = RegularUserManager()

    class Meta:
        proxy = True


class ModeratorUserManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MODERATOR)


class ModeratorUser(User):
    base_type = User.Types.COMMON

    objects = ModeratorUserManager()

    class Meta:
        proxy = True
