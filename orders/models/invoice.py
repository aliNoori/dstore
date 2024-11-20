from decimal import Decimal
from django.db import models
from django.utils import timezone
from orders.models.order import Order
from orders.models.shippingmethod import ShippingMethod
from products.models.product import Product
from users.models.address import Address
from users.models.customuser import CustomUser

class Invoice(models.Model):
    # ارتباط با سفارش
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice', null=True, blank=True)
    # ارتباط با یوزر
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invoices', default=0)
    # شماره فاکتور
    invoice_number = models.CharField(max_length=50, unique=True)
    # تاریخ صدور فاکتور
    issue_date = models.DateTimeField(auto_now_add=True)
    # تاریخ سررسید
    due_date = models.DateTimeField()
    # مجموع مبلغ فاکتور
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sub_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # tax_rate
    tax_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # مالیات
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # تخفیف
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #روش ارسال هرینه
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # وضعیت پرداخت
    status = models.CharField(max_length=20, default='pending')
    # توضیحات اضافی
    #notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # مقداردهی اولیه به tax و total_amount اگر None باشند
        if self.tax is None:
            self.tax = 0.00

        if not self.invoice_number:
            today = timezone.now().strftime('%Y%m%d')
            last_invoice = Invoice.objects.filter(invoice_number__startswith=today).order_by('invoice_number').last()
            if last_invoice:
                last_number = int(last_invoice.invoice_number.split('-')[-1])
                self.invoice_number = f"{today}-{last_number + 1:04d}"
            else:
                self.invoice_number = f"{today}-0001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ['-issue_date']  # مرتب‌سازی بر اساس تاریخ صدور به ترتیب نزولی


class InvoiceItem(models.Model):
    # ارتباط با فاکتور
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    # نام محصول یا خدمت
    description = models.CharField(max_length=255)
    # مقدار محصول یا خدمت
    quantity = models.PositiveIntegerField()
    # قیمت واحد
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # مجموع قیمت (quantity * unit_price)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    discount=models.DecimalField(max_digits=5, decimal_places=2)

    price_with_discount=models.DecimalField(max_digits=10, decimal_places=2)



    def save(self, *args, **kwargs):
        # محاسبه مجموع قیمت هنگام ذخیره‌سازی
        self.total = self.quantity * self.price
        if self.discount:
            self.price_with_discount = self.total * (1 - self.discount / 100)
        else:
            self.price_with_discount = self.total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.quantity} @ {self.price} each"

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"
        ordering = ['invoice', 'description']  # مرتب‌سازی بر اساس فاکتور و نام محصول
