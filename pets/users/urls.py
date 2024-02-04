from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from users import views

urlpatterns = [
    path("signup/", views.signup, name='signup'),
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True,
                                                next_page=(reverse_lazy('homepage')),
                                                template_name="auth/signin-modal.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('homepage')), name='logout'),
    path("profile/edit/", views.EditProfileView.as_view(), name='edit-profile'),
    path("profile/<int:pk>", views.UserProfileView.as_view(), name='profile'),
]
