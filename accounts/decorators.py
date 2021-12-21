from django.http import HttpResponse
from django.shortcuts import redirect

def is_user_authenticated(View_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return View_function(request, *args, **kwargs)

    return wrapper


def allowed_users(allowed=[]):
    def decorator(View_function):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed:
                return View_function(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return  wrapper
    return decorator
