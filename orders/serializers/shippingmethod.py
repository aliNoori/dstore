from rest_framework import serializers
from files.models.file import File
from orders.models.shippingmethod import ShippingMethod


class ShippingMethodSerializer(serializers.ModelSerializer):    

    image = serializers.ImageField(required=False)  # فیلد تصویر اختیاری

   
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'description', 'cost','delivery_time','is_active','image'] 

    def create(self, validated_data):
            # ایجاد آدرس با ارتباط به کاربر
        shippingMethod = ShippingMethod.objects.create(
            
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            cost=validated_data.get('cost'),
            delivery_time=validated_data.get('delivery_time'),
            is_active=validated_data.get('is_active'),
            
        )

        # اگر تصویر وجود داشته باشد
        image = validated_data.get('image', None)
        if image:
            File.objects.create(shippingMethod=shippingMethod, file=image)

        return shippingMethod
    

    def update(self,instance,validated_data):

       instance.name=validated_data.get('name', instance.name)
       instance.description=validated_data.get('description', instance.description)
       instance.cost=validated_data.get('cost', instance.cost)
       instance.delivery_time=validated_data.get('delivery_time', instance.delivery_time)
       instance.is_active=validated_data.get('is_active', instance.is_active)


        # مدیریت تصویر
       image = validated_data.get('image', None)
       if image:
           # حذف تصویر قبلی اگر وجود داشته باشد
           old_file = File.objects.filter(shippingMethod=instance).first()
           if old_file:
                old_file.delete()

           # ذخیره تصویر جدید
           File.objects.create(shippingMethod=instance, file=image)
    

       return instance
