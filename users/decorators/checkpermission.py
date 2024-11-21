from functools import wraps
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

def hasPermission(permission):
    def decorator(view_func):
        # بررسی اینکه دکوراتور فقط برای کلاس‌های APIView استفاده می‌شود
        if not isinstance(view_func, type) or not issubclass(view_func, APIView):
            raise TypeError("The @hasPermission decorator can only be applied to APIView classes.")

        # تزئین متد dispatch برای مدیریت درخواست‌ها
        original_dispatch = view_func.dispatch

        @wraps(view_func)
        def dispatch_wrapper(self, request, *args, **kwargs):
            # بررسی احراز هویت
            if not hasattr(request, 'auth') or request.auth is None:
                if not request.user or not request.user.is_authenticated:
                    raise NotAuthenticated(detail="Authentication required")

            # بررسی دسترسی
            if not request.user.has_perm(permission):
                raise PermissionDenied(detail="Access denied")

            # ادامه اجرای view اصلی
            return original_dispatch(self, request, *args, **kwargs)

        view_func.dispatch = dispatch_wrapper
        return view_func

    return decorator
