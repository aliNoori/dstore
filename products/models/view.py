from django.db import models
from products.models.product import Product
from users.models import CustomUser


class View(models.Model):
    # کاربری که محصول را مشاهده کرده است (می‌تواند تهی باشد)
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='views'
    )
    
    # محصولی که مشاهده شده است
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='views'
    )

    # ثبت زمان مشاهده
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # مرتب‌سازی پیش‌فرض بر اساس زمان ایجاد
        ordering = ['-created_at']
        verbose_name = "View"
        verbose_name_plural = "Views"

    def __str__(self):
        # نمایش کاربر و محصول در زمان نمایش مدل به عنوان رشته
        return f"View by {self.user} on {self.product}"
