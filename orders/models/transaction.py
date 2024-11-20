from django.db import models
from orders.models.order import Order
#from users.models.wallet import Wallet  # فرض بر این است که مدل Wallet دارید

class Transaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='transaction', null=True, blank=True)  # تراکنش مربوط به سفارش   
    transaction_type = models.CharField(max_length=20)  # نوع تراکنش
    amount = models.DecimalField(max_digits=15, decimal_places=2)  # مبلغ تراکنش
    status = models.CharField(max_length=20, default='pending')  # وضعیت تراکنش
    
    # فیلدهای جدید
    token = models.CharField(max_length=50, blank=True, null=True)  # توکن تراکنش
    terminal_no = models.CharField(max_length=50, blank=True, null=True)  # شماره ترمینال
    rrn = models.CharField(max_length=50, blank=True, null=True)  # شماره رسید
    tsp_token = models.CharField(max_length=50, blank=True, null=True)  # توکن TSP
    hash_card_number = models.CharField(max_length=100, blank=True, null=True)  # شماره کارت هش شده
    sw_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # مبلغ نهایی پرداخت شده
    strace_no = models.CharField(max_length=50, blank=True, null=True)  # شماره ردیابی
    redirect_url = models.URLField(max_length=200, blank=True, null=True)  # آدرس بازگشت
    callback_error = models.CharField(max_length=200, blank=True, null=True)  # خطای بازگشت
    verify_error = models.CharField(max_length=200, blank=True, null=True)  # خطای تایید
    reverse_error = models.CharField(max_length=200, blank=True, null=True)  # خطای بازگشت وجه

    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد تراکنش
    updated_at = models.DateTimeField(auto_now=True)  # تاریخ به‌روزرسانی تراکنش

    def __str__(self):
        return f"{self.get_transaction_type_display()} of {self.amount} - {self.status}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-created_at']  # مرتب‌سازی بر اساس تاریخ ایجاد به ترتیب نزولی
