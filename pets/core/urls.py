"""
URL configuration for pets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from core import views
from users import error_views

urlpatterns = [
    path("", views.IndexView.as_view(), name="homepage"),
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls"))
]

# Error pages
urlpatterns += [
    path("forbidden/", error_views.permission_denied, name="forbidden"),
    path("not-found/", error_views.page_not_found, name="not-found"),
    path("bad-request/", error_views.bad_request, name="bad-request"),
    path("internal/", error_views.server_error, name="internal"),
]

handler400 = 'users.error_views.bad_request'
handler403 = 'users.error_views.permission_denied'
handler404 = 'users.error_views.page_not_found'
handler500 = 'users.error_views.server_error'
