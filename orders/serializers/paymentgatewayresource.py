from rest_framework import serializers
from orders.models.paymentgateway import PaymentGateway


class CustomImageField(serializers.Field):
    def to_representation(self, value):
        if value:
            # Assuming the File model stores the image's file path in `file` field
            return {"path": value.file.url}  # Adjust this based on your file URL/path logic
        return None

class PaymentGatewayResource(serializers.ModelSerializer):
    
    image = CustomImageField(source='file')  # Assuming a user has a related file through `file_set`
          
    class Meta:
        model = PaymentGateway
        fields = ['id', 'gateway','type', 'description','is_active',
                  'terminal_id','wsdl','wsdl_confirm','wsdl_reverse'
                  ,'wsdl_multiplexed','payment_gateway','image'] 

        
    def get_image(self, obj):
              
        return obj.image     