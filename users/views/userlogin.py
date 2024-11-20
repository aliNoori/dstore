# users/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password  # اضافه کردن برای بررسی هش رمز عبور
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models.customuser import CustomUser  # مدل کاربر شما

class UserLoginView(APIView):
    def post(self, request):
        # دریافت داده‌های ورودی (ایمیل و رمز عبور)
        email = request.data.get('email')
        password = request.data.get('password')

        # بررسی اینکه آیا ایمیل و رمز عبور وجود دارند
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # پیدا کردن کاربر از طریق ایمیل
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # بررسی صحت رمز عبور
        if not check_password(password, user.password):  # بررسی هش رمز عبور
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # تولید توکن‌های JWT در صورت موفقیت
        refresh = RefreshToken.for_user(user)
        return Response({"token": str(refresh.access_token)}, status=status.HTTP_200_OK)








#with username


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from users.models.customuser import CustomUser  # مدل کاربر شما

# class UserLoginView(APIView):
#     def post(self, request):
#         # دریافت داده‌های ورودی (ایمیل و رمز عبور)
#         username = request.data.get('username')
#         print(username)
#         password = request.data.get('password')
#         print(password)
#         # بررسی اینکه آیا ایمیل و رمز عبور وجود دارند
#         if not username or not password:
#             return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # پیدا کردن کاربر از طریق ایمیل
#             user = CustomUser.objects.get(username=username)
            
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         # بررسی صحت رمز عبور
#         user = authenticate(request, email=username, password=password)
#         print(user)
#         if user is not None:
#             # تولید توکن‌های JWT در صورت موفقیت
#             refresh = RefreshToken.for_user(user)
#             return Response({"token":str(refresh.access_token)},status=status.HTTP_200_OK)
#             # return Response({
#             #     "refresh": str(refresh),
#             #     "access": str(refresh.access_token),
#             #     "user": {
#             #         "id": user.id,
#             #         "username": user.username,
#             #         "email": user.email,
#             #     }
#             # }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
