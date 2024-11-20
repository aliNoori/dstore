from django.db import models
from orders.models.order import Order  # فرض اینکه مدل Order در فایل جداگانه‌ای تعریف شده است
from products.models.product import Product  # فرض اینکه مدل Product در فایل جداگانه‌ای تعریف شده است

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='details')
    quantity = models.IntegerField()  # تعداد محصول
    price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت واحد محصول در زمان سفارش
    total = models.DecimalField(max_digits=10, decimal_places=2)  # مبلغ کل برای این آیتم

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # محاسبه مبلغ کل قبل از ذخیره
        self.total = self.quantity * self.price
        super(OrderDetail, self).save(*args, **kwargs)

    def __str__(self):
        return f"OrderDetail {self.id} - Order {self.order.id} - Product {self.product.name}"
