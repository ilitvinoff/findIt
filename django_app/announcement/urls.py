from django.urls import path

from announcement.views import CategoriesView, AnnouncementListView, AnnouncementDetailView

urlpatterns = [
    path("", AnnouncementListView.as_view(), name='announcement-list'),
    path("root-categories/", CategoriesView.as_view(is_root=True), name='root-categories'),
    path("categories/<int:pk>/", CategoriesView.as_view(), name='categories'),
    path("<pk>/", AnnouncementDetailView.as_view(), name="announcement-detail"),
]
