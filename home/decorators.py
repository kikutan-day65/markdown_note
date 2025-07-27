from functools import wraps

from django.http import JsonResponse

from home.messages import LOGIN_REQUIRED


def forbid_anonymous(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "error": LOGIN_REQUIRED}, status=403)
        return view_func(request, *args, **kwargs)

    return wrapper
