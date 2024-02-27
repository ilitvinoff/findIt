from django.contrib import admin
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


@admin.register(AnnouncementImage)
class AnnouncementImageAdmin(admin.ModelAdmin):
    ordering = ("announcement", )
