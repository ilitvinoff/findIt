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
    from users.models import User
    from announcement.models import Announcement
    from announcement.models import AnnouncementImage

    path = "tmp"
    instance_type = type(instance)

    if instance_type is User:
        path = "unknown_user_type"

        if instance.type == User.Types.COMMON:
            path = "common_user"
        elif instance.type == User.Types.MODERATOR:
            path = "moderator_user"

    elif instance_type is Announcement:
        path = f"announcement_{instance.owner.id}"

    elif instance_type is AnnouncementImage:
        path = f"announcement_{instance.announcement.owner.id}_{instance.announcement.id}"

    return "{path}/{filename}".format(path=path, filename=filename)