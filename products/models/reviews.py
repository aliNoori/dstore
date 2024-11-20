from django.db import models
from products.models.product import Product
from users.models import CustomUser

class Review(models.Model):
    # کاربر ثبت‌کننده نظر
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviews'
    )

    # محصولی که نظر مربوط به آن است
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )

    # امتیاز کاربر به محصول (مقدار بین 1 تا 5)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00
    )

    # متن نظر کاربر
    review = models.TextField(null=True, blank=True)

    # وضعیت تایید نظر (به‌صورت پیش‌فرض تایید نشده)
    is_approved = models.BooleanField(default=False)

    # زمان ایجاد و به‌روزرسانی نظر
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # جلوگیری از ثبت بیش از یک نظر برای هر کاربر برای هر محصول
        unique_together = ('user', 'product')
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']  # مرتب‌سازی نظرات به ترتیب نزولی زمان

    def __str__(self):
        # نمایش نظر با کاربر و محصول مرتبط به همراه امتیاز
        return f"Review by {self.user} on {self.product.name} - Rating: {self.rating}"
