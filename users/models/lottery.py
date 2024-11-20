from django.db import models
from users.models.customuser import CustomUser
from orders.models.order import Order

class Lottery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lottery_entries')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lottery_entries')
    entry_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)  # دلیل اضافه شدن به لاتاری
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Order {self.order.pk}"

    class Meta:
        verbose_name = "Lottery Entry"
        verbose_name_plural = "Lottery Entries"
        ordering = ['-entry_date']
