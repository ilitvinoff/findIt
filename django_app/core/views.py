from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.core.paginator import Paginator

from announcement.models import Category, Announcement


class IndexView(TemplateView):
    http_method_names = ["get"]
    template_name = "index.html"
    extra_context = {}

    ANNOUNCEMENTS_PER_PAGE = 12

    def get(self, request, *args, **kwargs):
        announcements = Announcement.objects.all().order_by("-updated")
        paginator = Paginator(announcements, self.ANNOUNCEMENTS_PER_PAGE)
        page_number = request.GET.get("page", 1)
        filtered_data = {"page": page_number + 1}
        self.extra_context.update({
            "category_hierarchy": Category.objects.roots(),
            "announcements_page": paginator.page(page_number),
            "filter_data": urlencode(filtered_data),
        })
        return super(IndexView, self).get(request, *args, **kwargs)
