from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models.wallet import Wallet
from users.serializers.walletresource import WalletResource


class MyWalletView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):
        # بازیابی همه‌ی آدرس‌های مرتبط با کاربر جاری
        wallet = Wallet.objects.filter(user=request.user).first()
        
        # سریالایز کردن آدرس‌ها
        wallet_data = WalletResource(wallet).data
        
        # ارسال پاسخ با داده‌های سریالایز شده
        return Response({'wallet':wallet_data}, status=status.HTTP_200_OK)
