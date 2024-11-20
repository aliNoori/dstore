from rest_framework import serializers

from products.models.history import History


class HistoryResource(serializers.ModelSerializer):


    class Meta:
        model = History
        fields = ['id','price_history','changed_at']