from rest_framework import serializers
from files.models.file import File
from orders.models.paymentgateway import PaymentGateway
from orders.models.paymentmethod import PaymentMethod


class PaymentGatewaySerializer(serializers.ModelSerializer):    

    image = serializers.ImageField(required=False)  # فیلد تصویر اختیاری

   
    class Meta:
        model = PaymentGateway
        fields = ['id', 'gateway','type', 'description','is_active',
                  'terminal_id','wsdl','wsdl_confirm','wsdl_reverse'
                  ,'wsdl_multiplexed','payment_gateway','image'] 

    def create(self, validated_data):
            # ایجاد آدرس با ارتباط به کاربر
        paymentGateway = PaymentGateway.objects.create(
            
            gateway=validated_data.get('gateway'),
            type=validated_data.get('type'),
            description=validated_data.get('description'),
            is_active=validated_data.get('is_active'),
            terminal_id=validated_data.get('terminal_id'),
            wsdl=validated_data.get('wsdl'),
            wsdl_confirm=validated_data.get('wsdl_confirm'),
            wsdl_reverse=validated_data.get('wsdl_reverse'),
            wsdl_multiplexed=validated_data.get('wsdl_multiplexed'),
            payment_gateway=validated_data.get('payment_gateway'),
            
        )

        # اگر تصویر وجود داشته باشد
        image = validated_data.get('image', None)
        if image:
            File.objects.create(paymentGateway=paymentGateway, file=image)

        return paymentGateway
    

    def update(self,instance,validated_data):

       instance.gateway=validated_data.get('gateway', instance.gateway)
       instance.type=validated_data.get('type', instance.type)
       instance.description=validated_data.get('description', instance.description)
       instance.is_active=validated_data.get('is_active', instance.is_active)
       instance.terminal_id=validated_data.get('terminal_id', instance.terminal_id)
       instance.wsdl=validated_data.get('wsdl', instance.wsdl)
       instance.wsdl_confirm=validated_data.get('wsdl_confirm', instance.wsdl_confirm)
       instance.wsdl_reverse=validated_data.get('wsdl_reverse', instance.wsdl_reverse)
       instance.wsdl_multiplexed=validated_data.get('wsdl_multiplexed', instance.wsdl_multiplexed)
       instance.payment_gateway=validated_data.get('payment_gateway', instance.payment_gateway)      


        # مدیریت تصویر
       image = validated_data.get('image', None)
       if image:
           # حذف تصویر قبلی اگر وجود داشته باشد
           old_file = File.objects.filter(paymentGateway=instance).first()
           if old_file:
                old_file.delete()

           # ذخیره تصویر جدید
           File.objects.create(paymentGateway=instance, file=image)
    

       return instance
