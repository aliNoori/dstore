from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from orders.models.paymentmethod import PaymentMethod
from orders.models.shippingmethod import ShippingMethod
from orders.serializers.paymentmethod import PaymentMethodSerializer
from orders.serializers.paymentmethodresource import PaymentMethodResource


class CreatePaymentMethodView(APIView):
    
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request):
        # ایجاد Serializer و اعتبارسنجی داده‌ها
        serializer = PaymentMethodSerializer(data=request.data)

        if serializer.is_valid():
            # ذخیره آدرس در صورتی که داده‌ها معتبر باشند
            paymentMethod = serializer.save()

            # سریالایز کردن داده‌های آدرس ذخیره‌شده
            paymentMethod_data = PaymentMethodResource(paymentMethod).data

            return Response(paymentMethod_data, status=status.HTTP_200_OK)
        
        # در صورت عدم اعتبار داده‌ها، پیام خطا برگردانده می‌شود
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePaymentMethodView(APIView):
    
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request,id):

        address=PaymentMethod.objects.get(id=id)
        # ایجاد Serializer و اعتبارسنجی داده‌ها
        serializer = PaymentMethodSerializer(address,data=request.data,partial=True)

        if serializer.is_valid():
            # ذخیره آدرس در صورتی که داده‌ها معتبر باشند
            paymentMethod = serializer.save()

            # سریالایز کردن داده‌های آدرس ذخیره‌شده
            paymentMethod_data = PaymentMethodResource(paymentMethod).data

            return Response(paymentMethod_data, status=status.HTTP_200_OK)
        
        # در صورت عدم اعتبار داده‌ها، پیام خطا برگردانده می‌شود
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PaymentMethodListView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):
        # بازیابی همه‌ی آدرس‌های مرتبط با کاربر جاری
        paymentMethods = PaymentMethod.objects.all()
        
        # سریالایز کردن آدرس‌ها
        paymentMethods_data = PaymentMethodResource(paymentMethods, many=True).data
        
        # ارسال پاسخ با داده‌های سریالایز شده
        return Response({'paymentMethods':paymentMethods_data}, status=status.HTTP_200_OK)


        
        