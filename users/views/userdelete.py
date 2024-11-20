# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models import CustomUser

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def delete(self, request, id):
        # پیاده‌سازی برای حذف یک کاربر خاص
        try:
            user = CustomUser.objects.get(id=id)  # فرض بر اینکه User مدل کاربران است
            user.delete()
            return Response({'message': 'User deleted'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
