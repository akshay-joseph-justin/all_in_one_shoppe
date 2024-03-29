from django.shortcuts import redirect
from functools import wraps


def redirect_authenticated_user(view, redirect_to='users:profile-update'):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('mod:home')
            return redirect(redirect_to, name=request.user.username)
        else:
            return view(request, *args, **kwargs)
    return wrapper


def only_authenticated_user(view, redirect_to='users:login'):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect(redirect_to)
        else:
            return view(request, *args, **kwargs)
    return wrapper
