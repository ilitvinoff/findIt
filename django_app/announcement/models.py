from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.postgres.expressions import ArraySubquery
from django.db import models
from django.db.models import Count, OuterRef
from django.db.models.functions import JSONObject
from django.utils.translation import gettext_lazy as _

from core.models import CoreModel, ThumbnailModel
from core.utils import get_storage_path, select_storage

User = get_user_model()


class CategoryQuerySet(models.QuerySet):
    raw_query = """
                WITH RECURSIVE folks(id, name, parent_id) AS (
                    SELECT id, name, parent_id, 0 as depth
                    FROM announcement_category
                    WHERE id=%s
                    UNION ALL
                    SELECT c.id, c.name, c.parent_id, f.depth + 1 AS depth
        			FROM announcement_category c
        			{join_clause}
        			{depth_clause}
        		)
                SELECT *
                FROM folks
                ORDER BY DEPTH {order}
                """

    def with_ancestors(self, pk, depth=None):
        depth_clause = "" if depth is None or type(depth) is not int else f"WHERE f.depth < {depth}"
        join_clause = "INNER JOIN folks f ON f.parent_id = c.id "
        query = self.raw_query.format(depth_clause=depth_clause, join_clause=join_clause, order="DESC")
        return self.raw(query, [pk])

    def with_descendants(self, pk, depth=None):
        depth_clause = "" if depth is None or type(depth) is not int else f"WHERE f.depth < {depth}"
        join_clause = "INNER JOIN folks f ON f.id = c.parent_id "
        query = self.raw_query.format(depth_clause=depth_clause, join_clause=join_clause, order="ASC")
        return self.raw(query, [pk])

    def get_all_hierarchy_including_children(self, pk):
        query = """
                WITH RECURSIVE ancestors(id, name, parent_id) AS (
                    SELECT id, name, parent_id, 0 as depth, name::varchar as path, ARRAY(SELECT ROW(s.id, s.name, s.parent_id) FROM announcement_category s WHERE s.parent_id=a.parent_id OR (s.parent_id is NULL AND a.parent_id IS NULL)) AS siblings
                    FROM announcement_category a
                    WHERE id=%s
                    UNION ALL
                    SELECT c.id, c.name, c.parent_id, f.depth - 1 AS depth, c.name::varchar || ' / ' || f.path::varchar, ARRAY(SELECT ROW(s1.id, s1.name, s1.parent_id) FROM announcement_category s1 WHERE  s1.parent_id=c.parent_id  OR (s1.parent_id is NULL AND c.parent_id IS NULL)) AS siblings
                    FROM announcement_category c
                    INNER JOIN ancestors f ON f.parent_id = c.id 
                )
                SELECT a.id, a.name, a.parent_id, a.depth, siblings, ARRAY (SELECT ROW(d.id, d.name, d.parent_id) FROM announcement_category d WHERE d.parent_id=%s) as children
                FROM ancestors a
                ORDER BY depth
                """

        raw_queryset = self.raw(query, [pk, pk])
        for c in raw_queryset:
            siblings = []
            children = []
            for s in c.siblings:
                siblings.append(Category(id=s[0], name=s[1]))
            for ch in c.children:
                children.append(Category(id=ch[0], name=ch[1]))
            c.siblings = siblings
            c.children = children

        return raw_queryset

    def roots(self):
        return self.filter(parent=None)

    def leafs(self):
        return self.annotate(children_count=Count("descendants")).filter(children_count=0)

    def annotate_siblings(self):
        return self.annotate(siblings=
                             ArraySubquery(Category.objects.filter(parent=OuterRef("parent")).exclude(
                                 pk=OuterRef("pk")).distinct().values(
                                 json=JSONObject(id="id", name="name", parent="parent")))
                             )


class Category(CoreModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True, related_name="descendants")

    objects = CategoryQuerySet().as_manager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f'{self.name}_pk{{{self.pk}}}'

    @admin.display(description="Categories")
    def get_ancestors(self):
        return "->".join([e.name for e in self.__class__.objects.with_ancestors(self.pk)])


class Announcement(ThumbnailModel):
    title = models.CharField(_("Title"), max_length=100, null=False, blank=False)
    content = models.CharField(_("Description"), max_length=1200, null=True)
    price = models.FloatField(_("Price"), null=False, blank=False, default=0)
    poster = models.ImageField(upload_to=get_storage_path, blank=True, null=False, storage=select_storage)
    poster_preview = models.ImageField(upload_to=get_storage_path, blank=True, null=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="announcements")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name="categories")

    def get_image(self):
        return self._get_image(field_name="poster")

    def get_image_preview(self):
        return self._get_image(field_name="poster_preview")

    def get_price(self):
        return round(self.price, 2)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk or (update_fields and "poster" in update_fields):
            self._make_thumbnail("poster", "poster_preview")
        return super(Announcement, self).save(force_insert, force_update, using, update_fields)


class AnnouncementImage(ThumbnailModel):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, null=False, related_name="images")
    file = models.ImageField(upload_to=get_storage_path, blank=False, null=False, storage=select_storage)
    preview = models.ImageField(upload_to=get_storage_path, blank=True, null=False, storage=select_storage)

    def get_image(self):
        return self._get_image(field_name="file")

    def get_image_preview(self):
        return self._get_image(field_name="preview")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self._make_thumbnail("file", "preview")
        return super(AnnouncementImage, self).save(force_insert, force_update, using, update_fields)
