import django_filters
from django.db.models import Q

from announcement.models import Announcement, Category


class AnnouncementFilters(django_filters.FilterSet):
    a_contain = django_filters.CharFilter(method="announcement_contain")
    category = django_filters.NumberFilter(method="in_descendants")

    def announcement_contain(self, qs, name, value):
        return qs.filter(Q(title__icontains=value) | Q(content__icontains=value))

    def in_descendants(self, qs, name, value):
        return qs.filter(category__in=[c.id for c in Category.objects.with_descendants(value)])

    class Meta:
        model = Announcement
        fields = {
            "price": ["lte", "gte"],
        }
