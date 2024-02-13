from django.conf import settings
from django.core.files.storage import storages


def select_storage():
    if settings.USE_AWS:
        return storages["aws"]
    else:
        return storages["default"]


def get_storage_path(instance, filename):
    # must return Unix-style path (with forward slashes)
    # more at https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FileField.upload_to
    dirname = "tmp"
    from users.models import User

    instance_type = type(instance)

    if instance_type is User:
        dirname = "unknown_user_type"

        if instance.type == User.Types.COMMON:
            dirname = "common_user"
        elif instance.type == User.Types.MODERATOR:
            dirname = "moderator_user"

    return "{instance}/{filename}".format(instance=dirname, filename=filename)