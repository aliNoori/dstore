from rest_framework import serializers


from users.models.wallet import Wallet

class WalletResource(serializers.ModelSerializer):
    
        
   
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'created_at','updated_at'] 