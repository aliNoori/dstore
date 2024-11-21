from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models.customuser import CustomUser

class ToggleGroup(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, email):
        # یافتن کاربر بر اساس ایمیل
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({'success': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # استخراج نقش (گروه) از درخواست
        group_name = request.data.get('role')  # فرض می‌کنیم داده به این صورت ارسال شده
        if not group_name:
            return Response({'success': False, 'message': 'Role is required'}, status=status.HTTP_400_BAD_REQUEST)

        # یافتن گروه یا ارسال خطا در صورت عدم وجود
        group = get_object_or_404(Group, name=group_name)

        # بررسی اینکه آیا کاربر در گروه است یا نه
        if group in user.groups.all():
            # اگر کاربر در گروه است، حذف کن
            user.groups.remove(group)
            message = f"{user.name} removed from group {group_name}"
        else:
            # اگر کاربر در گروه نیست، اضافه کن
            user.groups.add(group)
            message = f"{user.name} added to group {group_name}"

        # ارسال پاسخ
        return Response({'success': True, 'message': message}, status=status.HTTP_200_OK)
