from django.db import models
from users.models.customuser import CustomUser

class Coupon(models.Model):
    # ارتباط با کاربر
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='coupons')
    # نام کوپن
    code = models.CharField(max_length=50, unique=True)
    # تاریخ انقضا کوپن
    expire_date = models.DateTimeField()
    # درصد تخفیف یا مقدار تخفیف ثابت
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # نوع تخفیف (درصدی یا ثابت)
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='fixed')
    # وضعیت استفاده از کوپن (استفاده شده یا نشده)
    is_used = models.BooleanField(default=False)
    # توضیحات اضافی
    description = models.TextField(null=True, blank=True)



    def __str__(self):
        return f"Coupon {self.code} - {self.discount_amount} ({self.get_discount_type_display()})"



    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        ordering = ['-expire_date']  # مرتب‌سازی بر اساس تاریخ انقضا به ترتیب نزولی
