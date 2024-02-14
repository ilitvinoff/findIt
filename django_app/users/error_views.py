from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'errors/not-found.html', {})


def server_error(request):
    return render(request, 'errors/internal.html', {})


def permission_denied(request, exception):
    return render(request, 'errors/forbidden.html', {})


def bad_request(request, exception):
    return render(request, 'errors/bad-request.html', {})
