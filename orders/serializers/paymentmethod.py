from rest_framework import serializers
from files.models.file import File
from orders.models.paymentmethod import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):    

    image = serializers.ImageField(required=False)  # فیلد تصویر اختیاری

   
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'description','is_active','image'] 

    def create(self, validated_data):
            # ایجاد آدرس با ارتباط به کاربر
        paymentMethod = PaymentMethod.objects.create(
            
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            is_active=validated_data.get('is_active'),
            
        )

        # اگر تصویر وجود داشته باشد
        image = validated_data.get('image', None)
        if image:
            File.objects.create(paymentMethod=paymentMethod, file=image)

        return paymentMethod
    

    def update(self,instance,validated_data):

       instance.name=validated_data.get('name', instance.name)
       instance.description=validated_data.get('description', instance.description)
       instance.is_active=validated_data.get('is_active', instance.is_active)


        # مدیریت تصویر
       image = validated_data.get('image', None)
       if image:
           # حذف تصویر قبلی اگر وجود داشته باشد
           old_file = File.objects.filter(paymentMethod=instance).first()
           if old_file:
                old_file.delete()

           # ذخیره تصویر جدید
           File.objects.create(paymentMethod=instance, file=image)
    

       return instance
