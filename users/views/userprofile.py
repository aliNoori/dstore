# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.serializers.userresource import UserResource


class UserProfileView(APIView):
    
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):

        user=request.user

        user_data=UserResource(user).data
        # پیاده‌سازی برای مشاهده پروفایل کاربر
        return Response(user_data, status=status.HTTP_200_OK)
