# myapp/views.py

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from carts.models.cart import Cart
from carts.serializers.cartresource import CartResource


class CartItemsShow(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)
    def get(self, request):
        #cart = Cart.objects.filter(user=request.user)Array
        cart = Cart.objects.filter(user=request.user).first()  # گرفتن اولین سبد کاربر
        cart_data = CartResource(cart).data
        return Response({"cart":cart_data}, status=status.HTTP_200_OK)
    