from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from orders.models.shippingmethod import ShippingMethod
from orders.serializers.shippingmethod import ShippingMethodSerializer
from orders.serializers.shippingmethodresource import ShippingMethodResource


class CreateShippingMethodView(APIView):
    
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request):
        # ایجاد Serializer و اعتبارسنجی داده‌ها
        serializer = ShippingMethodSerializer(data=request.data)

        if serializer.is_valid():
            # ذخیره آدرس در صورتی که داده‌ها معتبر باشند
            shippingMethod = serializer.save()

            # سریالایز کردن داده‌های آدرس ذخیره‌شده
            shippingMethod_data = ShippingMethodResource(shippingMethod).data

            return Response(shippingMethod_data, status=status.HTTP_200_OK)
        
        # در صورت عدم اعتبار داده‌ها، پیام خطا برگردانده می‌شود
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateShippingMethodView(APIView):
    
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request,id):

        address=ShippingMethod.objects.get(id=id)
        # ایجاد Serializer و اعتبارسنجی داده‌ها
        serializer = ShippingMethodSerializer(address,data=request.data,partial=True)

        if serializer.is_valid():
            # ذخیره آدرس در صورتی که داده‌ها معتبر باشند
            shippingMethod = serializer.save()

            # سریالایز کردن داده‌های آدرس ذخیره‌شده
            shippingMethod_data = ShippingMethodResource(shippingMethod).data

            return Response(shippingMethod_data, status=status.HTTP_200_OK)
        
        # در صورت عدم اعتبار داده‌ها، پیام خطا برگردانده می‌شود
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ShippingMethodListView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):
        # بازیابی همه‌ی آدرس‌های مرتبط با کاربر جاری
        shippingMetods = ShippingMethod.objects.all()
        
        # سریالایز کردن آدرس‌ها
        shippingMethods_data = ShippingMethodResource(shippingMetods, many=True).data
        
        # ارسال پاسخ با داده‌های سریالایز شده
        return Response({'shippingMethods':shippingMethods_data}, status=status.HTTP_200_OK)


        
        