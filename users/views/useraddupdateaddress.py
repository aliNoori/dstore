from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models.address import Address
from users.serializers.address import AddressSerializer
from users.serializers.addressresource import AddressResource


class UserAddAddressView(APIView):
    
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request):
        # ایجاد Serializer و اعتبارسنجی داده‌ها
        serializer = AddressSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # ذخیره آدرس در صورتی که داده‌ها معتبر باشند
            address = serializer.save()

            # سریالایز کردن داده‌های آدرس ذخیره‌شده
            address_data = AddressResource(address).data

            return Response(address_data, status=status.HTTP_200_OK)
        
        # در صورت عدم اعتبار داده‌ها، پیام خطا برگردانده می‌شود
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateAddressView(APIView):
    
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request,id):

        address=Address.objects.get(id=id)
        # ایجاد Serializer و اعتبارسنجی داده‌ها
        serializer = AddressSerializer(address,data=request.data,partial=True)

        if serializer.is_valid():
            # ذخیره آدرس در صورتی که داده‌ها معتبر باشند
            address = serializer.save()

            # سریالایز کردن داده‌های آدرس ذخیره‌شده
            address_data = AddressResource(address).data

            return Response(address_data, status=status.HTTP_200_OK)
        
        # در صورت عدم اعتبار داده‌ها، پیام خطا برگردانده می‌شود
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        
        