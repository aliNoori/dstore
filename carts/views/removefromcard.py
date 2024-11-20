# myapp/views.py

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models.product import Product
from carts.models.cart import Cart
from carts.models.cartitem import CartItem



class RemoveFromCart(APIView):

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
            cart_item.quantity -= 1
            if cart_item.quantity<=0:
                cart_item.delete()
            else:    
                cart_item.save()
                return Response({"message": "Product added to cart successfully", "quantity": cart_item.quantity}
                                , status=status.HTTP_200_OK)
        else:
            return Response({"message": "Item not found in cart"},
                             status=status.HTTP_400_BAD_REQUEST)
        
        