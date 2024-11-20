from rest_framework import serializers


from orders.models.invoice import InvoiceItem
from products.serializers.productresource import ProductResource

class InvoiceItemResource(serializers.ModelSerializer): 

    product=ProductResource()
    
    class Meta:
        model = InvoiceItem
        fields = ['id', 'product', 'description', 'quantity',
                   'price','total','discount','price_with_discount']


    # You can add custom validation or methods here if necessary 
