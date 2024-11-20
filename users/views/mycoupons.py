from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from users.models.coupon import Coupon
from users.serializers.couponresource import CouponResource


class MyCouponsView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):
        # بازیابی همه‌ی آدرس‌های مرتبط با کاربر جاری
        coupons = Coupon.objects.filter(user=request.user)
        
        # سریالایز کردن آدرس‌ها
        coupons_data = CouponResource(coupons, many=True).data
        
        # ارسال پاسخ با داده‌های سریالایز شده
        return Response({'coupons':coupons_data}, status=status.HTTP_200_OK)
