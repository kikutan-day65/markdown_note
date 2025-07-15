from functools import wraps

from django.http import JsonResponse


def forbid_anonymous(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"success": False, "error": "Forbidden: Login required"}, status=403
            )
        return view_func(request, *args, **kwargs)

    return wrapper
