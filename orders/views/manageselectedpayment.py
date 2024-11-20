from orders.models.paymentgateway import PaymentGateway
from orders.models.paymentmethod import PaymentMethod
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.serializers.paymentgatewayresource import PaymentGatewayResource
from orders.views.paymentgateway import PaymentGatewayListView

class ManageSelectedPaymentView(APIView):
    def post(self, request, payment_method_id):
        user = request.user

        # دریافت متد پرداخت
        payment_method = PaymentMethod.objects.filter(id=payment_method_id).first()
        ###change type to name
        # بررسی نوع متد پرداخت
        if payment_method:
            if payment_method.name == 'credit_card':
                # عملیات مخصوص برای کارت اعتباری
                action = "Processing credit card payment"
            elif payment_method.name == 'paypal':
                # عملیات مخصوص برای PayPal
                action = "Processing PayPal payment" 
            elif payment_method.name == 'Online':
                # عملیات مخصوص برای Online
                action = "Online"
            elif payment_method.name == 'Offline':
                # عملیات مخصوص برای Offline
                action = "Processing Offline payment"           
            elif payment_method.name == 'wallet':
                # عملیات مخصوص برای wallet
                action = "Processing wallet payment"
            elif payment_method.name == 'bank_transfer':
                # عملیات مخصوص برای انتقال بانکی
                action = "Processing bank transfer payment"
            elif payment_method.name == 'cash_on_delivery':
                # عملیات مخصوص پرداخت درب منزل
                action = "Processing cash on delivery"
            else:
                action = "Unknown payment method"
        else:
            return Response({
                'success': False,
                'message': 'Payment method not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        # بازگرداندن نتیجه نهایی
        return Response({
            'success': True,
            'action': action,
        }, status=status.HTTP_200_OK)
