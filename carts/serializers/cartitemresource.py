from rest_framework import serializers

from products.serializers.productresource import ProductResource
from carts.models.cartitem import CartItem



class CartItemResource(serializers.ModelSerializer):

    product=ProductResource()
    
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product']

 
    # You can add custom validation or methods here if necessary
