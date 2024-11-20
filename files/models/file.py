from django.db import models
from django.conf import settings
import os
from orders.models.paymentgateway import PaymentGateway
from orders.models.paymentmethod import PaymentMethod
from orders.models.shippingmethod import ShippingMethod
from products.models.category import Category
from products.models.product import Product
from users.models.customuser import CustomUser

# Create your models here.
class File(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='file')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='file')
    category=models.OneToOneField(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='file')
    shippingMethod=models.OneToOneField(ShippingMethod, on_delete=models.CASCADE, null=True, blank=True, related_name='file')
    paymentMethod=models.OneToOneField(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True, related_name='file')
    paymentGateway=models.OneToOneField(PaymentGateway, on_delete=models.CASCADE, null=True, blank=True, related_name='file')
    file = models.ImageField(upload_to='files/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File {self.id} - {self.file.name}"
    
    def delete(self, *args, **kwargs):
        # Delete the file from the media folder
        if self.file:
            file_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)  # حذف فایل از سیستم فایل
        super(File, self).delete(*args, **kwargs)  # سپس رکورد را از دیتابیس حذف کن
