# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):
        # پیاده‌سازی برای لیست کاربران
        return Response({'users': 'List of users'}, status=status.HTTP_200_OK)

# سایر view‌ها نیز مشابه خواهند بود...
