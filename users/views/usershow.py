# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import CustomUser
from users.serializers.userresource import UserResource

class UserShowView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request, id):
        # پیاده‌سازی برای نمایش یک کاربر خاص
        # فرض بر این است که شما یک مدل User دارید که اطلاعات کاربران را نگه می‌دارد
        try:
            user = CustomUser.objects.get(id=id)  # فرض بر اینکه User مدل کاربران است
            # سریالایز کردن اطلاعات کاربر
            json = UserResource(user)
            # بازگرداندن داده‌های سریالایز شده
            return Response(json.data)
            # return Response({'user': {
            #     'id': user.id,
            #     'username': user.username,
            #     'email': user.email
            # }}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
