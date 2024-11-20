from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models.address import Address
from users.serializers.address import AddressSerializer


class UserAddressListView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):
        # بازیابی همه‌ی آدرس‌های مرتبط با کاربر جاری
        addresses = Address.objects.filter(user=request.user)
        
        # سریالایز کردن آدرس‌ها
        serializer = AddressSerializer(addresses, many=True)
        
        # ارسال پاسخ با داده‌های سریالایز شده
        return Response({'addresses':serializer.data}, status=status.HTTP_200_OK)
