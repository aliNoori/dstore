from django.db import models
from products.models.product import Product
from users.models import CustomUser

class Like(models.Model):
    # کاربری که لایک را انجام داده است (می‌تواند تهی باشد)
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='likes'
    )

    # محصولی که لایک شده است
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )

    # زمان ایجاد لایک
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # جلوگیری از ثبت لایک تکراری توسط یک کاربر برای یک محصول
        unique_together = ('user', 'product')
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        ordering = ['-created_at']  # مرتب‌سازی لایک‌ها بر اساس زمان

    def __str__(self):
        # نمایش کاربر و محصول در زمان نمایش مدل به عنوان رشته
        return f"Like by {self.user} on {self.product}"
