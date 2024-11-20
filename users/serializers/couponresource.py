from rest_framework import serializers
from users.models.coupon import Coupon

class CouponResource(serializers.ModelSerializer):
    
        
   
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'expire_date', 'discount_amount','discount_type', 'is_used', 'description'] 