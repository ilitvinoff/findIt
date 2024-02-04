from django.http import HttpResponseServerError
from django.views import generic
from django.contrib.auth import login, get_user_model, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

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


class UserProfileView(generic.TemplateView):
    template_name = "users/common_user/profile.html"
    http_method_names = ['get', 'delete']
    instance = None
    extra_context = {}

    SHOW_CONTACTS = "show_contacts"

    @staticmethod
    def _is_owner(user, pk):
        if not user:
            return False
        return user.pk == pk

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        self.instance = user
        context.update({'profile': user})

        return context

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        is_owner = self._is_owner(request.user, pk)
        request_method = request.method.lower()

        if request_method == "get":
            if is_owner:
                self.extra_context.update({self.SHOW_CONTACTS: True})

        elif request_method == "delete":
            if is_owner:
                user_to_delete = request.user
                logout(request)
                User.objects.filter(pk=user_to_delete.pk).delete()
                return redirect(reverse_lazy("homepage"))

            return HttpResponseServerError()

        return super(UserProfileView, self).dispatch(request, *args, **kwargs)


class EditProfileView(generic.TemplateView):
    http_method_names = ['get', 'put']
    template_name = "users/common_user/edit-profile.html"