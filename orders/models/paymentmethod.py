from django.db import models

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    type=models.CharField(max_length=100,null=True)
    description = models.TextField(blank=True, null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

    @property
    def image(self):
       if self.file:  # اطمینان از وجود فایل
            return self.file.file.url  # دسترسی به URL فایل
       return None  # در صورت نبودن فایل، None برگردانید

