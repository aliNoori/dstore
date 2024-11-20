from rest_framework import serializers
from users.models.address import Address

class AddressResource(serializers.ModelSerializer):
    
        
   
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state','country', 'postal_code', 'is_default'] 