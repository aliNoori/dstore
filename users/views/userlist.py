# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models.customuser import CustomUser
from users.serializers.userresource import UserResource  # فرض می‌کنیم سریالایزر شما همین نام دارد

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):
        # دریافت لیست تمام کاربران
        users = CustomUser.objects.all()

        # سریالایز کردن داده‌ها
        users = UserResource(users, many=True).data

        # بازگرداندن لیست سریالایزشده
        return Response({'users_list': users}, status=status.HTTP_200_OK)
