from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from orders.models.invoice import Invoice,InvoiceItem
from orders.models.order import Order
from orders.models.shippingmethod import ShippingMethod
from orders.serializers.invoiceresource import InvoiceResource
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal


class InvoiceCreate(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self,request,order_number):

        #get user
        user=request.user

        # بررسی وجود سفارش با استفاده از شماره سفارش
        order = Order.objects.filter(user=user, order_number=order_number).first()

        if not order:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # دریافت آیتم‌های سفارش
        order_items = order.details.all()
         # تنظیم روش ارسال و هزینه حمل
        shipping_cost = Decimal('0.00')
        shipping_method = None
        shipping_method_id = order.shipping_method_id
        print(shipping_method_id)
        if shipping_method_id:
            shipping_method = ShippingMethod.objects.filter(id=shipping_method_id).first()
            print(shipping_method)
        if shipping_method:
            shipping_cost = shipping_method.cost
            print(shipping_cost)

        # محاسبه مبلغ کل فاکتور
        #sub_total_amount = sum(item.product.price * item.quantity for item in cart_items)


        # بررسی فاکتورهای موجود
        #existing_invoice = Invoice.objects.filter(user=user, payment_status='Pending').first()
        # if existing_invoice:
        #     # بررسی اینکه آیا آیتم‌های سبد خرید تغییری کرده‌اند
        #     existing_invoice_items = existing_invoice.items.all()
        #     if (len(existing_invoice_items) == len(cart_items) and 
        #         all(item.product == existing_item.product and item.quantity == existing_item.quantity 
        #             for item, existing_item in zip(cart_items, existing_invoice_items))):
        #         # اگر تغییری مشاهده نشود، همان فاکتور قبلی را بازگردانید
        #         json=InvoiceSerializer(existing_invoice)
        #         # بازگرداندن داده‌های سریالایز شده
        #         return Response(json.data)# ایجاد فاکتور جدید در صورتی که تغییری وجود داشته باشد یا فاکتور جدیدی ایجاد شود
        invoice = Invoice.objects.create(
        #invoice_number save in model in method(save)
        order=order,
        status='Pending',  # وضعیت فاکتور به عنوان "در انتظار" (پرداخت نشده)
        due_date=timezone.now() + timezone.timedelta(days=30),  # تاریخ سررسید
        shipping_cost=shipping_cost,
        sub_total_amount=0,
        total_amount=0
        )

    
        invoice.save()

        subTotalAmount=0

        # ایجاد آیتم‌های فاکتور
        for item in order_items:
            invoice_item=InvoiceItem.objects.create(
            invoice=invoice,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            #total save in model in method(save)
            discount=item.product.discount or Decimal(0),  # در صورت عدم وجود تخفیف، مقدار 0 قرار داده می‌شود
            #price_with_discount save in model in method(save)
            description='',  # توضیحات در صورت نیاز
            )

            subTotalAmount+=invoice_item.price_with_discount  # محاسبه مقدار با تخفیف پس از ایجاد آیتم

        #محاسبه نرخ مالیات
        # محاسبه نرخ مالیات با استفاده از Decimal
        tax_rate = Decimal('10')  # تبدیل نرخ مالیات به Decimal
        tax = subTotalAmount * (tax_rate / Decimal('100'))  # محاسبه مالیات
        total_amount=subTotalAmount+tax+shipping_cost 


        # به‌روزرسانی فاکتور با استفاده از save
        invoice.sub_total_amount = subTotalAmount
        invoice.tax_rate = tax_rate
        invoice.tax = tax
        invoice.total_amount = total_amount
        invoice.save()  # ذخیره تغییرات در فاکتور
  

        invoice_data=InvoiceResource(invoice).data
        return Response({"invoice":invoice_data}, status=status.HTTP_201_CREATED)  

        
            
        


        

        
        

