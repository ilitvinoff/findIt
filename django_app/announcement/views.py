from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from announcement.filters import AnnouncementFilters
from announcement.models import Category, Announcement


class CategoriesView(TemplateView):
    http_method_names = ["get"]
    template_name = "announcements/partial/categories/selector.html"
    extra_context = {}
    is_root = False

    def get(self, request, *args, **kwargs):
        if self.is_root:
            self.template_name = "announcements/partial/categories/root_selector.html"
            self.extra_context.update({"category_hierarchy": Category.objects.roots()})

        else:
            pk = self.kwargs.get("pk")
            if pk is None:
                raise AttributeError(
                    "Category detail view %s must be called with either an "
                    "pk in the URLconf." % self.__class__.__name__
                )

            category_hierarchy = Category.objects.get_all_hierarchy_including_children(pk)
            self.extra_context.update({"category_hierarchy": category_hierarchy})

        return super(CategoriesView, self).get(request, *args, **kwargs)


class AnnouncementList(TemplateView):
    http_method_names = ["post", "get"]
    template_name = "announcements/partial/list.html"
    PER_PAGE = 12
    extra_context = {}

    def get(self, request, *args, **kwargs):
        data = request.GET.copy()
        f = AnnouncementFilters(data, queryset=Announcement.objects.all().order_by("-updated"))
        p = Paginator(f.qs, self.PER_PAGE)
        page = p.get_page(data.get("page", 1))

        data["page"] = page.number + 1
        context = self.get_context_data(**kwargs)
        context.update({"announcements_page": page, "filter_data": urlencode(data)})
        return self.render_to_response(context)

