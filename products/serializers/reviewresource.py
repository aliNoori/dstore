from rest_framework import serializers

from products.models.history import History
from products.models.reviews import Review


class ReviewResource(serializers.ModelSerializer):


    class Meta:
        model = Review
        fields = ['id','rating','review']