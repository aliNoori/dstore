from django.db import models
from users.models.customuser import CustomUser
from products.models.product import Product

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')  # کاربر صاحب سبد خرید
    #products = models.ManyToManyField(Product, through='CartItem', related_name='carts')  # محصولات در سبد خرید با استفاده از مدل CartItem
    quantity = models.PositiveIntegerField(default=1)  # تعداد محصول در سبد خرید
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد سبد خرید
    updated_at = models.DateTimeField(auto_now=True)  # تاریخ آخرین به‌روزرسانی سبد خرید

    def __str__(self):
        return f"Cart of {self.user.username}"
    

    # متد برای خالی کردن سبد خرید پس از ایجاد سفارش
    def clear_cart(self):
        #self.items.update(status='ordered')  # تغییر وضعیت آیتم‌ها به سفارش شده
        self.items.all().delete()  # حذف همه آیتم‌ها از سبد خرید

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ['-created_at']  # مرتب‌سازی سبدها بر اساس تاریخ ایجاد به ترتیب نزولی
