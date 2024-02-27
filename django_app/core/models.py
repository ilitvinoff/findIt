from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _


class CoreModel(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"))

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"


class ThumbnailModel(CoreModel):
    class Meta:
        abstract = True

    def _get_image(self, field_name="image", default=f"{settings.STATIC_URL}assets/images/empty.png"):
        try:
            image_field = getattr(self, field_name)
            if image_field and image_field.url:
                return image_field.url
        except ValueError:
            pass

        return default

    def _make_thumbnail(self, src_field_name="image", dst_field_name="image_preview"):
        image_field = getattr(self, src_field_name)
        dst_field = getattr(self, dst_field_name)
        if image_field and image_field.url:
            try:
                image = Image.open(image_field)
            except:
                raise ValidationError({src_field_name: 'bad image value'})

            image.thumbnail(settings.MEDIA_THUMB_SIZE, Image.LANCZOS)

            thumb_filename = 'thumb_' + image_field.name

            temp_thumb = BytesIO()
            try:
                image.save(temp_thumb, image.format)
            except:
                raise ValidationError({src_field_name: 'bad image format'})

            temp_thumb.seek(0)

            # set save=False, otherwise it will run in an infinite loop
            dst_field.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()
