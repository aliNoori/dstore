from rest_framework import serializers
from products.models.reviews import Review
from products.serializers.productresource import ProductResource
from users.serializers.userresource import UserResource


class ReviewResource(serializers.ModelSerializer):

    user = UserResource()  # سریالایزر کامل برای کاربر

    class Meta:
        model = Review
        fields = ['id','rating','review','user']