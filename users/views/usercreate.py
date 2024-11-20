# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers.createupdateuser import CreateUpdateUserFormSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers.userresource import UserResource

class UserCreateView(APIView):

    def post(self, request):
        serializer = CreateUpdateUserFormSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.save()  # ذخیره کاربر جدید

            # تولید توکن‌های JWT برای کاربر تازه ثبت‌نام شده
            refresh = RefreshToken.for_user(user)
            # سریالایز کردن اطلاعات کاربر
            user_data = UserResource(user).data

            # اضافه کردن توکن‌ها به داده‌های سریالایز شده
            #user_data['refresh'] = str(refresh)
            user_data['token'] = str(refresh.access_token)
            # بازگرداندن داده‌های سریالایز شده
            return Response(user_data, status=status.HTTP_200_OK)
            # return Response({
            #     "user": RegisterUserFormSerializer(user).data,
            #     "refresh": str(refresh),
            #     "access": str(refresh.access_token),
            # }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
