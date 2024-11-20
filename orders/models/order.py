from django.utils import timezone
from django.db import models
from users.models.address import Address
from users.models.customuser import CustomUser

class Order(models.Model):
    # ORDER_STATUS_CHOICES = [
    #     ('pending', 'Pending'),         # در انتظار
    #     ('processing', 'Processing'),   # در حال پردازش
    #     ('shipped', 'Shipped'),         # ارسال شده
    #     ('delivered', 'Delivered'),     # تحویل داده شده
    #     ('canceled', 'Canceled'),       # لغو شده
    # ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')  # کاربری که سفارش را ثبت کرده
    address=models.ForeignKey(Address,on_delete=models.CASCADE,related_name='order')
    order_number = models.CharField(max_length=20, unique=True)  # شماره یکتا برای سفارش
    #status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')  # وضعیت سفارش
    status = models.CharField(max_length=20, default='pending')  # وضعیت سفارش
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # مجموع قیمت سفارش
    comments = models.TextField(null=True, blank=True)  # نظرات اضافی    
    shipping_method_id = models.BigIntegerField(null=True)  # روش ارسال یا تکمیل سفارش
    payment_method_id = models.BigIntegerField(null=True)  # روش ارسال یا تکمیل سفارش
    resource_payment=models.CharField(max_length=50)#    
    order_date = models.DateTimeField(auto_now_add=True)  # تاریخ ثبت سفارش
    shipped_date = models.DateTimeField(null=True, blank=True)  # تاریخ ارسال
    delivered_date = models.DateTimeField(null=True, blank=True)  # تاریخ تحویل


    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-order_date']  # مرتب‌سازی بر اساس تاریخ سفارش، از جدید به قدیم
