from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from users.forms import SignUpForm


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
