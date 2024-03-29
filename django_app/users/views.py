from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseServerError
from django.views import generic
from django.contrib.auth import login, get_user_model, logout, views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from announcement.models import Announcement
from users import forms
from users.forms import SignUpForm

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy("homepage"))

        return render(request, "auth/signup-modal.html", form.get_context(), )

    elif request.method == 'GET':
        form = SignUpForm()

        return render(request, "auth/signup-modal.html", form.get_context(), )


class UserLoginView(auth_views.LoginView):
    template_name = "auth/signin-modal.html"
    next_page = reverse_lazy('homepage')
    redirect_authenticated_user = True

    def form_valid(self, form):
        auth_views.auth_login(self.request, form.get_user())
        self.template_name = "auth/partials/success-sign-in.html"
        return self.render_to_response(None)

    def form_invalid(self, form):
        self.template_name = "auth/partials/sign-in-form.html"
        return super(UserLoginView, self).form_invalid(form)


class UserProfileView(generic.TemplateView):
    template_name = "users/common_user/profile.html"
    http_method_names = ['get', 'delete']
    extra_context = {}

    ANNOUNCEMENTS_PER_PAGE = 21

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        context.update({'profile': user})

        return context

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        request_method = request.method.lower()

        if request_method == "get":
            data = request.GET.copy()
            qs = Announcement.objects.filter(owner=pk).order_by("-updated")
            p = Paginator(qs, self.ANNOUNCEMENTS_PER_PAGE)
            page = p.get_page(data.get("page", 1))
            self.extra_context.update({"announcements_page": page, "filter_data": urlencode(data)})

        elif request_method == "delete":
            if is_owner:
                user_to_delete = request.user
                logout(request)
                User.objects.filter(pk=user_to_delete.pk).delete()
                return redirect(reverse_lazy("homepage"))

            return HttpResponseServerError()

        return super(UserProfileView, self).dispatch(request, *args, **kwargs)


class EditProfileView(LoginRequiredMixin, generic.TemplateView):
    http_method_names = ['get', 'post']
    template_name = "users/common_user/edit-profile.html"
    extra_context = {}

    def dispatch(self, request, *args, **kwargs):
        request_method = request.method.lower()

        if request_method == "get":
            form = forms.BaseUserEditForm(instance=get_object_or_404(User, pk=request.user.id))
            self.extra_context.update({"form": form})

        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = forms.BaseUserEditForm(request.POST, request.FILES,
                                      instance=get_object_or_404(User, pk=request.user.id))
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("profile", kwargs={'pk': request.user.id}))

        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)
