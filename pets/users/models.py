from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CoreModel


class CustomUserManager(UserManager):
    def _create_user(self, email, password=None, username=None, **extra_fields):
        if not username:
            username = User.normalize_username(username)
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.

        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("type", [User.Types.ADMIN])

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, CoreModel):
    class Types(models.IntegerChoices):
        ADMIN = (0, "Administrator")
        COMMON = (1, "Common user")
        MODERATOR = (2, "Moderator")

    base_type = Types.COMMON

    email = models.EmailField(_("Email"), blank=False, null=False, unique=True)
    username = models.EmailField(_("Username"), blank=False, null=True, unique=True)
    type = models.IntegerField(_("Type"), choices=Types.choices)

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
        return super(User, self).save(*args, **kwargs)


class RegularUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COMMON)


class CommonUser(User):
    base_type = User.Types.COMMON

    objects = RegularUserManager()

    class Meta:
        proxy = True


class ModeratorUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MODERATOR)


class ModeratorUser(User):
    base_type = User.Types.COMMON

    objects = ModeratorUserManager()

    class Meta:
        proxy = True
