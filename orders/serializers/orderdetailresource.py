from rest_framework import serializers

from orders.models.orderdetail import OrderDetail
from products.serializers.productresource import ProductResource


class OrderDetailResource(serializers.ModelSerializer):

    product=ProductResource()

    class Meta:
        model = OrderDetail
        fields = ['id','product', 'quantity','price','total','product']


    # You can add custom validation or methods here if necessary 


