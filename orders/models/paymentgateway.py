from django.db import models

class PaymentGateway(models.Model):
    gateway = models.CharField(max_length=100)
    type=models.CharField(max_length=100,null=True)
    description = models.TextField(blank=True, null=True)
    is_active=models.BooleanField(default=True)
    terminal_id = models.CharField(max_length=100, unique=True)  # Unique terminal ID for the payment gateway
    wsdl = models.TextField(blank=True, null=True)  # WSDL URL for initiating payments
    wsdl_confirm = models.CharField(max_length=255, blank=True, null=True)  # WSDL URL for confirming payments
    wsdl_reverse = models.CharField(max_length=255, blank=True, null=True)  # WSDL URL for reversing payments
    wsdl_multiplexed = models.CharField(max_length=255, blank=True, null=True)  # WSDL URL for multiplexed payments
    payment_gateway = models.CharField(max_length=100)  # Identifier for the payment gateway
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the gateway was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the gateway was last updated

    def __str__(self):
        return self.gateway

    class Meta:
        verbose_name = "Gateway Payment"
        verbose_name_plural = "Gateway Payments"
        ordering = ['-created_at']  # Order by creation date, newest first
    

    @property
    def image(self):
       if self.file:  # اطمینان از وجود فایل
            return self.file.file.url  # دسترسی به URL فایل
       return None  # در صورت نبودن فایل، None برگردانید

