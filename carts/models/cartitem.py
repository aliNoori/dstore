from django.db import models
from carts.models import Cart
from products.models.product import Product  # فرض بر این است که مدل Product دارید


# مدل میانی برای مدیریت محصولات در سبد خرید
class CartItem(models.Model):
    # STATUS_CHOICES = [
    #     ('in_cart', 'In Cart'),
    #     ('ordered', 'Ordered'),
    # ]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # ارتباط با سبد خرید
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField(default=1)  # تعداد محصول در سبد خرید
    #status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='in_cart')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
