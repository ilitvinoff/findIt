from django.contrib import admin
from django.forms import ModelChoiceField

from .models import Category, Announcement, AnnouncementImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["get_ancestors"]
    autocomplete_fields = ["parent"]
    ordering = ["name"]
    search_fields = ["name"]


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    ordering = ("created",)

    def save_model(self, request, obj, form, change):
        update_fields = []

        if change:
            for initial_field, initial_value in form.initial.items():
                if form.cleaned_data[initial_field] != initial_value:
                    if isinstance(form.fields[initial_field], ModelChoiceField) and initial_value==getattr(form.cleaned_data[initial_field], "id"):
                        continue
                    update_fields.append(initial_field)

        obj.save(update_fields=update_fields)


@admin.register(AnnouncementImage)
class AnnouncementImageAdmin(admin.ModelAdmin):
    ordering = ("announcement",)
