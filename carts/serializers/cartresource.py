from rest_framework import serializers


from carts.models.cart import Cart
from carts.serializers.cartitemresource import CartItemResource


class CartResource(serializers.ModelSerializer):

    items=CartItemResource(many=True)  
    count=serializers.SerializerMethodField()  
    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'updated_at','items','count']

    def get_count(self, obj):
              
        return obj.items.count()    


    # You can add custom validation or methods here if necessary
