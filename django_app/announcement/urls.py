from django.urls import path

from announcement.views import CategoriesView, AnnouncementList

urlpatterns = [
    path("", AnnouncementList.as_view(), name='announcement-list'),
    path("root-categories/", CategoriesView.as_view(is_root=True), name='root-categories'),
    path("categories/<int:pk>/", CategoriesView.as_view(), name='categories'),
]
