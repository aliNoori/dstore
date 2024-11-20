# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models import CustomUser
from users.serializers.createupdateuser import CreateUpdateUserFormSerializer
from users.serializers.userresource import UserResource

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # دریافت داده‌های ورودی و استفاده از serializer برای به‌روزرسانی
        serializer = CreateUpdateUserFormSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            user=serializer.save()
            # سریالایز کردن اطلاعات کاربر
            user_data = UserResource(user).data
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
