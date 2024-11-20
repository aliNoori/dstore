from rest_framework import serializers

from orders.models.invoice import Invoice
from orders.serializers.invoiceitemresource import InvoiceItemResource

class InvoiceResource(serializers.ModelSerializer): 

    
    items=InvoiceItemResource(many=True)
    
    class Meta:
        model = Invoice
        fields = ['id','order','invoice_number','status', 'issue_date', 'due_date',
                   'sub_total_amount','tax_rate','tax','shipping_cost','total_amount','items']


    # You can add custom validation or methods here if necessary 
