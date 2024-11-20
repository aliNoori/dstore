from django.db import models

from products.models.category import Category

# Create your models here.
class Product (models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')  # ارتباط با دسته‌بندی
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    sku=models.CharField(max_length=255,null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # اصلاح شده
    created_at = models.DateTimeField(auto_now_add=True)  # این فیلد را اضافه کنید
    updated_at = models.DateTimeField(auto_now=True)  # این فیلد را اضافه کنید
    

    def __str__(self):
        return self.name
    
    @property
    def image(self):
        return self.file.first().file.url  # اولین فایل مرتبط با محصول را بازمی‌گرداند