from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from users import views

urlpatterns = [
    path("signup/", views.signup, name='signup'),
    path("login/", views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('homepage')), name='logout'),
    path("profile/edit/", views.EditProfileView.as_view(), name='edit-profile'),
    path("profile/<int:pk>", views.UserProfileView.as_view(), name='profile'),
]
