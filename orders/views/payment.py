from datetime import datetime
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from orders.gateways.mellat import MellatGateway
from orders.gateways.melli import MelliGateway
from orders.gateways.persian import ParsianGateway
from orders.interfaces.paymentgatewayinterface import PaymentGatewayInterface
from orders.models.invoice import Invoice
from orders.models.order import Order
from orders.models.paymentgateway import PaymentGateway
from orders.models.transaction import Transaction
from users.tasks import add_gift_to_user, add_score, apply_coupon, charge_wallet, handle_high_value_order, send_payment_notification



def payment(gateway: PaymentGatewayInterface, amount, order_id, callback_url):
    return gateway.process_payment(amount, order_id, callback_url)

class ProcessPaymentView(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, order_number, gateway_id):

        try:
            gateway = PaymentGateway.objects.get(id=gateway_id)
        except PaymentGateway.DoesNotExist:
            return Response({"message": "Gateway not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # یافتن فاکتور مربوطه
        order = Order.objects.filter(order_number=order_number).first()
        if order is None:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        invoice = order.invoice
        amount = int(invoice.total_amount)  # تبدیل به عدد اعشاری

        if gateway.gateway == 'parsian':
            gateway_selected = ParsianGateway()
        elif gateway.gateway == 'mellat':
            gateway_selected = MellatGateway()
        elif gateway.gateway == 'melli':
            gateway_selected = MelliGateway()
        else:
            return Response({"message": "Unsupported payment gateway"}, status=status.HTTP_400_BAD_REQUEST)

        ##callback_url = 'http://127.0.0.1:8000/api/callback/payment/'
        callback_url='http://192.168.1.100:8000/api/callback/payment/'

        # استفاده از تابع payment برای انجام پرداخت
        try:
            url = payment(gateway_selected, amount, order.id, callback_url)
            # ارسال URL به فرانت‌اند به‌صورت JSON
            return Response({"url": url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class CallbackPaymentView(APIView):

    def post(self,request):     
        # Check if the user is authenticated
        #if not request.user.is_authenticated:
        #return redirect('user_login')  # Redirect to the login page or handle accordingly    
        # دسترسی به فیلدهای موجود در POST data
        status = request.POST.get('status')
        token = request.POST.get('Token')
        order_id = request.POST.get('OrderId')
        terminal_no = request.POST.get('TerminalNo')
        rrn = request.POST.get('RRN')
        tsp_token = request.POST.get('TspToken')
        hash_card_number = request.POST.get('HashCardNumber')
        sw_amount = request.POST.get('SwAmount')
        strace_no = request.POST.get('STraceNo')
        redirect_url = request.POST.get('RedirectURL')
        callback_error = request.POST.get('CallbackError')
        verify_error = request.POST.get('VerifyError')
        reverse_error = request.POST.get('ReverseError')

        error_message = None
        transaction = None
        # مقداردهی اولیه متغیر transaction_data به یک دیکشنری خالی
        transaction_data = {}

        if status == '0':
            # ایجاد تراکنش جدید
            transaction = Transaction.objects.create(
            transaction_type='payment',
            amount=sw_amount.replace(',', ''),  # تبدیل مبلغ به مقدار عددی
            status='completed',
            token=token,
            order_id=order_id,
            terminal_no=terminal_no,
            rrn=rrn,
            tsp_token=tsp_token,
            hash_card_number=hash_card_number,
            sw_amount=sw_amount.replace(',', ''),
            strace_no=strace_no,
            redirect_url=redirect_url,
            callback_error=callback_error,
            verify_error=verify_error,
            reverse_error=reverse_error,
        )
             # دریافت سفارش یا برگرداندن خطا
            order = get_object_or_404(Order, id=order_id)
            
            # بروزرسانی وضعیت سفارش
            order.status = 'processing'
            order.save()
        

            # موفقیت آمیز
            # پیدا کردن فاکتور بر اساس OrderId
            invoice = get_object_or_404(Invoice, order_id=order.pk, status='Pending')
            invoice.status = 'Completed'
            invoice.save()


            transaction.order=invoice.order
            transaction.save()


            ###########################  Queue  ############
            # امتیاز پایه
            base_score = 10
            reason='Base Score'
            description='Initial base score for the payment'
            add_score.delay(order.user_id,base_score,reason,description)


            #################### بررسی مشتری جدید
            if not Order.objects.filter(user_id=order.user_id).exclude(pk=order.pk).exists():

                initial_order_score = 50  ####### امتیاز ویژه برای اولین سفارش
                reason='First Order'
                description='Bonus for the first order'
                add_score.delay(order.user_id,initial_order_score,reason,description)
                ####### اولین سفارش - ارائه هدیه، ورود به قرعه‌کشی و غیره
                add_gift_to_user.delay(order.pk)


             ########################## بررسی سفارش‌های با ارزش بالا
            sw_amount = request.POST.get('SwAmount').replace(',', '')

            if float(sw_amount) > 1000:  # Example: threshold is 1000

                high_value_score = 20  # امتیاز اضافه برای سفارش‌های با مبلغ بالا
                reason='High Value Order'
                description='Bonus for order amount greater than 1000'
                add_score.delay(order.user_id,high_value_score,reason,description)

                handle_high_value_order.delay(order.pk)    


            ################## بررسی روزهای خاص
            today = datetime.today()
            if today.month == 10 and today.day == 31:  # مثال: کریسمس

                code="XMAS2024"

                special_day_score = 100  # امتیاز اضافه برای کریسمس

                reason='Special Day'
                description='Bonus for special day'

                add_score.delay(order.user_id,special_day_score,reason,description)
                apply_coupon.delay(order.pk, code)
                #if user have this coupon 50% and shipping free and ....    

            ################ شارژ کیف پول
            charge_wallet.delay(order.user_id, sw_amount.replace(',', ''))

            ################# ارسال اطلاع‌رسانی
            send_payment_notification.delay(order.user_id, order.pk)
        
            ################## ذخیره داده‌های تراکنش برای ارسال به فرانت‌اند
            transaction_data = {
                'order_id': order_id,
                'amount': sw_amount.replace(',', ''),
                'token': token,
                'rrn': rrn,
                'transaction_date': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }   
        
        elif status == '-1':
            error_message = "خطای سرور"
        elif status == '-130':
            error_message = "زمان توکن منقضی شده است"
        elif status == '-131':
            error_message = "توکن نامعتبر است"
        elif status == '-138':
            error_message = "توسط کاربر لغو شد"
        elif status == '-32768':
            error_message = "خطای ناشناخته رخ داده است"
        elif status == '-1528':
            error_message = "اطلاعات پرداخت یافت نشد"


        # بازگشت به صفحه پرداخت با پیام خطا و جزئیات تراکنش 
        query_params = {'error': error_message} if error_message else {}
        query_params.update(transaction_data)
        ##url = 'http://localhost:3000/your-transaction-receive'
        url='http://192.168.1.100/your-transaction-receive'
        redirect_url = f"{url}?{urlencode(query_params)}"

        return HttpResponseRedirect(redirect_url)
