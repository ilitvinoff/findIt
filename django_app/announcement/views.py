from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.http import HttpResponseServerError, HttpResponseForbidden
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from announcement.filters import AnnouncementFilters
from announcement.forms import AnnouncementCreateEditForm, AnnouncementImageFormsSetFactory, \
    AnnouncementImageUpdateFormsSetFactory
from announcement.models import Category, Announcement, AnnouncementImage


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


class AnnouncementListView(TemplateView):
    http_method_names = ["get"]
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


class AnnouncementDetailView(TemplateView):
    http_method_names = ["post", "get"]
    template_name = "announcements/detail.html"
    extra_context = {}

    def get(self, request, *args, **kwargs):
        a = get_object_or_404(Announcement, pk=kwargs.get("pk"))
        self.extra_context.update({
            "announcement": a,
            "photos": AnnouncementImage.objects.filter(announcement=a.id)
        })
        return super(AnnouncementDetailView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        a = get_object_or_404(Announcement, pk=kwargs.get("pk"))
        if request.user.is_authenticated and request.user.pk == a.owner.pk:
            try:
                a.delete()
                if request.headers.get("HX-Request"):
                    return HttpResponse(status=200)

                return redirect(reverse_lazy("profile", kwargs={"pk": request.user.pk}))

            except Exception as e:
                if request.headers.get("HX-Request"):
                    return HttpResponse(status=204)

                return HttpResponseServerError()

        return HttpResponseForbidden()


class AnnouncementCreateView(TemplateView):
    http_method_names = ["get", "post"]
    template_name = "announcements/create.html"
    image_formset = AnnouncementImageFormsSetFactory
    image_formset_queryset = AnnouncementImage.objects.none()
    category_hierarchy = Category.objects.roots()
    extra_context = {}
    instance = None
    form = AnnouncementCreateEditForm
    has_preset_category = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy("homepage"))
        return super(AnnouncementCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.extra_context.update({
            "form": self.form(instance=self.instance),
            "category_hierarchy": self.category_hierarchy,
            "has_preset_category": self.has_preset_category,
            "images_formset": self.image_formset(queryset=self.image_formset_queryset, instance=self.instance),
        })
        return super(AnnouncementCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES, instance=self.instance)
        image_formset = self.image_formset(request.POST, request.FILES, instance=self.instance)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.owner = request.user
            ann.save(update_fields=form.changed_data if ann.pk else None)

            if image_formset.is_valid():
                image_formset.instance = ann
                image_formset.save()

            return redirect(reverse_lazy("announcement-detail", kwargs={'pk': ann.id}))

        context = self.get_context_data()
        context["form"] = form

        if form.cleaned_data.get('category'):
            context["category_hierarchy"] = Category.objects.get_all_hierarchy_including_children(form.cleaned_data.get('category').pk)
            context['has_preset_category'] = True
        else:
            context["category_hierarchy"] = self.category_hierarchy

        return self.render_to_response(context)


class AnnouncementUpdateView(AnnouncementCreateView):
    template_name = "announcements/update.html"
    image_formset = AnnouncementImageUpdateFormsSetFactory
    has_preset_category = True

    def dispatch(self, request, *args, **kwargs):
        self.instance = get_object_or_404(Announcement, pk=kwargs.get("pk"))
        if not request.user.is_authenticated or request.user.pk != self.instance.owner.pk:
            return HttpResponseForbidden()

        self.image_formset_queryset = AnnouncementImage.objects.filter(announcement=self.instance.pk)
        self.category_hierarchy = Category.objects.get_all_hierarchy_including_children(self.instance.category.pk)
        return super(AnnouncementUpdateView, self).dispatch(request, *args, **kwargs)

