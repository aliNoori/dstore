# myapp/views.py

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from carts.serializers.cartresource import CartResource
from products.models.product import Product
from carts.models.cart import Cart
from carts.models.cartitem import CartItem


class AddToCart(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request,product_id):
        
        #product_id = request.data['product_id']

        product = get_object_or_404(Product, id=product_id)
        
        # پیدا کردن یا ایجاد سبد خرید برای کاربر
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # بررسی اینکه آیا این محصول قبلاً در سبد خرید کاربر وجود دارد یا نه
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            # اگر محصول قبلاً وجود داشت، تعداد آن را افزایش دهید
            cart_item.quantity += 1
            cart_item.save()
            cart_item_data=CartResource(cart).data
            return Response(cart_item_data,status=status.HTTP_200_OK)
        else:
            return Response({"message": "Cart item created"},status=status.HTTP_201_CREATED)

        
        