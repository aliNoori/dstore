
from django.db import models
from products.models.product import Product

class History(models.Model):
    # محصولی که قیمت آن تغییر کرده است
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='histories'
    )

    # قیمت ثبت شده در تاریخچه
    price_history = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )

    # زمان تغییر قیمت
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # مرتب‌سازی پیش‌فرض تاریخچه‌ها بر اساس زمان تغییر قیمت
        ordering = ['-changed_at']
        verbose_name = "Price History"
        verbose_name_plural = "Price Histories"

    def __str__(self):
        # نمایش قیمت و زمان تغییر
        return f"{self.product.name} - {self.price_history} (changed at {self.changed_at})"
