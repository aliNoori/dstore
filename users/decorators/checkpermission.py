from django.http import JsonResponse

class PermissionRequiredMixin:
    permission_required = None  # نام مجوز موردنیاز را اینجا مشخص کنید

    def dispatch(self, request, *args, **kwargs):
        # بررسی اینکه کاربر وارد سیستم شده است
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        # بررسی اینکه آیا کاربر مجوز لازم را دارد
        if self.permission_required and not request.user.has_perm(self.permission_required):
            return JsonResponse({'error': 'Access denied'}, status=403)

        # در صورتی که همه چیز درست باشد، ادامه اجرا
        return super().dispatch(request, *args, **kwargs)
