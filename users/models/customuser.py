from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser (AbstractUser):

    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    is_active=models.BooleanField(default=True)
    date_joined=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    @property
    def image(self):
        return self.file.first().file.url  # اولین فایل مرتبط با محصول را بازمی‌گرداند
