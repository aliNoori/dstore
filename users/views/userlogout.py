from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # احراز هویت کاربر نیاز است

    def get(self, request):
        try:
            user = request.user  # کاربر احراز هویت شده

            # یافتن و بلک‌لیست کردن تمام refresh_tokenهای مربوط به کاربر
            tokens = OutstandingToken.objects.filter(user=user)

            for token in tokens:
                # بررسی اینکه آیا توکن قبلاً بلک‌لیست شده است
                if not BlacklistedToken.objects.filter(token=token).exists():
                    # بلک‌لیست کردن توکن
                    BlacklistedToken.objects.create(token=token)

            return Response({"message": "Successfully logged out and tokens blacklisted"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
