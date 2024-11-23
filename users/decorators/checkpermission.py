from functools import wraps
from django.http import JsonResponse

def hasPermission(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            # مقداردهی request.user باید اینجا مقداردهی شده باشد
            if not hasattr(request, 'user') or request.user.is_anonymous:
                return JsonResponse({'error': 'Authentication required'}, status=401)

            if request.user.has_perm(permission):
                return view_func(self, request, *args, **kwargs)
            return JsonResponse({'error': 'Access denied'}, status=403)
        return _wrapped_view
    return decorator