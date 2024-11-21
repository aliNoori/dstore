from django.http import JsonResponse
from functools import wraps

def hasPermission(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.has_perm(permission):
                    return view_func(request, *args, **kwargs)
                else:
                    return JsonResponse({'detail': 'Access denied'}, status=403)  # پیام خطای دسترسی
            else:
                return JsonResponse({'detail': 'Authentication required'}, status=401)  # پیام خطای ورود
        return _wrapped_view
    return decorator
