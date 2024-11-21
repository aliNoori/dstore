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
            # بررسی احراز هویت با استفاده از request.auth (توکن)
            if not request.auth:  # اگر توکن در درخواست وجود نداشت
                raise NotAuthenticated(detail="Authentication required")

            # بررسی دسترسی کاربر بر اساس permission
            if not request.user.has_perm(permission):  # اگر کاربر مجوز لازم را نداشت
                raise PermissionDenied(detail="Access denied")

            # ادامه اجرای view اصلی
            return original_dispatch(self, request, *args, **kwargs)

        view_func.dispatch = dispatch_wrapper
        return view_func

    return decorator
