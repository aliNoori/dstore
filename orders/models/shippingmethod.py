from django.db import models

class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.CharField(max_length=100, blank=True, null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

    @property
    def image(self):
       if self.file:  # اطمینان از وجود فایل
            return self.file.file.url  # دسترسی به URL فایل
       return None  # در صورت نبودن فایل، None برگردانید

