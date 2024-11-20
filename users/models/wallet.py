from django.db import models
from users.models.customuser import CustomUser

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wallet')  # ارتباط یک به یک با کاربر
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # موجودی کیف پول
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد کیف پول
    updated_at = models.DateTimeField(auto_now=True)  # تاریخ آخرین به‌روزرسانی کیف پول

    def __str__(self):
        return f"Wallet of {self.user.username} - Balance: {self.balance}"

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        ordering = ['-created_at']  # مرتب‌سازی بر اساس تاریخ ایجاد به ترتیب نزولی
