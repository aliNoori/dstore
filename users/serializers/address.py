from rest_framework import serializers
from users.models.address import Address

class AddressSerializer(serializers.ModelSerializer):    
   
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state','country', 'postal_code', 'is_default'] 

    def create(self, validated_data):
        # گرفتن اطلاعات کاربر از `context`
        user = self.context['request'].user

        # ایجاد آدرس با ارتباط به کاربر
        address = Address.objects.create(
            user=user,
            street=validated_data.get('street'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            country=validated_data.get('country'),
            postal_code=validated_data.get('postal_code'),
            is_default=validated_data.get('is_default', False)
        )

        return address
    

    def update(self,instance,validated_data):

       instance.street=validated_data.get('street', instance.street)
       instance.city=validated_data.get('city', instance.city)
       instance.state=validated_data.get('state', instance.state)
       instance.country=validated_data.get('country', instance.country)
       instance.postal_code=validated_data.get('postal_code', instance.postal_code)
       instance.is_default=validated_data.get('is_default', instance.is_default)    


       return instance
