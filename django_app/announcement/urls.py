from django.urls import path

from announcement.views import CategoriesView, AnnouncementListView, AnnouncementDetailView, AnnouncementCreateView, \
    AnnouncementUpdateView

urlpatterns = [
    path("", AnnouncementListView.as_view(), name='announcement-list'),
    path("create/", AnnouncementCreateView.as_view(), name='announcement-create'),
    path("root-categories/", CategoriesView.as_view(is_root=True), name='root-categories'),
    path("categories/<int:pk>/", CategoriesView.as_view(), name='categories'),
    path("<pk>/update/", AnnouncementUpdateView.as_view(), name="announcement-update"),
    path("<pk>/", AnnouncementDetailView.as_view(), name="announcement-detail"),
]
