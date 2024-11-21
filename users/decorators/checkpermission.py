from functools import wraps
from rest_framework.views import APIView
from django.http import JsonResponse

def hasPermission(permission):
    def decorator(view_func):
        # بررسی اینکه دکوراتور فقط برای کلاس‌های APIView استفاده می‌شود
        if not isinstance(view_func, type) or not issubclass(view_func, APIView):
            raise TypeError("The @has_permission decorator can only be applied to APIView classes.")

        # تزئین متد dispatch برای مدیریت درخواست‌ها
        original_dispatch = view_func.dispatch

        @wraps(view_func)
        def dispatch_wrapper(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.has_perm(permission):
                    return original_dispatch(self, request, *args, **kwargs)
                else:
                    return JsonResponse({'detail': 'Access denied'}, status=403)
            else:
                return JsonResponse({'detail': 'Authentication required'}, status=401)

        view_func.dispatch = dispatch_wrapper
        return view_func

    return decorator
