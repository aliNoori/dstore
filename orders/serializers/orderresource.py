from rest_framework import serializers

from orders.models.order import Order
from orders.serializers.orderdetailresource import OrderDetailResource


class OrderResource(serializers.ModelSerializer):  

    
    #details=OrderDetailResource(many=True)
    items = OrderDetailResource(source='details', many=True)
    created_at=serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id','order_number','status', 'comments',
                   'shipping_method_id','payment_method_id','resource_payment','total_amount','items','created_at']
        

    def get_created_at(self, obj):
              
        return obj.order_date    
         


    # You can add custom validation or methods here if necessary 
