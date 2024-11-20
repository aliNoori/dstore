from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from orders.models.paymentgateway import PaymentGateway
from orders.serializers.paymentgateway import PaymentGatewaySerializer
from orders.serializers.paymentgatewayresource import PaymentGatewayResource


    

class CreatePaymentGatewayView(APIView):
    
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request):
        # ایجاد Serializer و اعتبارسنجی داده‌ها
        serializer = PaymentGatewaySerializer(data=request.data)

        if serializer.is_valid():
            # ذخیره آدرس در صورتی که داده‌ها معتبر باشند
            paymentGateway = serializer.save()

            # سریالایز کردن داده‌های آدرس ذخیره‌شده
            paymentGateway_data = PaymentGatewayResource(paymentGateway).data

            return Response(paymentGateway_data, status=status.HTTP_200_OK)
        
        # در صورت عدم اعتبار داده‌ها، پیام خطا برگردانده می‌شود
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePaymentGatewayView(APIView):
    
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request,id):

        address=PaymentGateway.objects.get(id=id)
        # ایجاد Serializer و اعتبارسنجی داده‌ها
        serializer = PaymentGatewaySerializer(address,data=request.data,partial=True)

        if serializer.is_valid():
            # ذخیره آدرس در صورتی که داده‌ها معتبر باشند
            paymentGateway = serializer.save()

            # سریالایز کردن داده‌های آدرس ذخیره‌شده
            paymentGateway_data = PaymentGatewayResource(paymentGateway).data

            return Response(paymentGateway_data, status=status.HTTP_200_OK)
        
        # در صورت عدم اعتبار داده‌ها، پیام خطا برگردانده می‌شود
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentGatewayListView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):
        # بازیابی همه‌ی آدرس‌های مرتبط با کاربر جاری
        onlineMethods = PaymentGateway.objects.all()
        
        # سریالایز کردن آدرس‌ها
        onlineMethods_data = PaymentGatewayResource(onlineMethods, many=True).data
        
        # ارسال پاسخ با داده‌های سریالایز شده
        return Response({'onlinePaymentMethods':onlineMethods_data}, status=status.HTTP_200_OK)


        
        