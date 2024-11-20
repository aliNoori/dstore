from rest_framework import serializers
from orders.models.paymentmethod import PaymentMethod


class CustomImageField(serializers.Field):
    def to_representation(self, value):
        if value:
            # Assuming the File model stores the image's file path in `file` field
            return {"path": value.file.url}  # Adjust this based on your file URL/path logic
        return None

class PaymentMethodResource(serializers.ModelSerializer):
    
    image = CustomImageField(source='file')  # Assuming a user has a related file through `file_set`
          
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'description','is_active','image'] 

        
    def get_image(self, obj):
              
        return obj.image     