from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string
from orders.models.order import Order
from orders.models.orderdetail import OrderDetail
from carts.models.cart import Cart
from orders.serializers.orderresource import OrderResource



class MyOrdersView(APIView):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).prefetch_related('orderdetails__product')
        orders_data = OrderResource(orders, many=True).data
        return Response({
            'success': True,
            'orders': orders_data,
        }, status=status.HTTP_200_OK)


class CreateOrderView(APIView):
    def post(self, request, address_id):
        user = request.user
        cart = Cart.objects.filter(user=user).prefetch_related('items__product').first()

        if not cart or not cart.items.exists():
            return Response({
                'success': False,
                'message': 'Cart is empty',
            }, status=status.HTTP_400_BAD_REQUEST)

        order_number = 'ORD-' + get_random_string(10)
        total_amount = 0
        order = Order.objects.create(
            user=user,
            address_id=address_id,
            order_number=order_number,
            status='pending',
            total_amount=0
        )

        for item in cart.items.all():
            item_total = item.quantity * item.product.price
            total_amount += item_total

            OrderDetail.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total=item_total
            )

        order.total_amount = total_amount
        order.save()

        cart.items.all().delete()

        order_data = OrderResource(order).data
        return Response({
            'success': True,
            'message': 'Order created successfully',
            'order': order_data,
        }, status=status.HTTP_201_CREATED)


class ShowOrderView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.prefetch_related('orderdetails__product').get(id=order_id)
        except Order.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Order not found',
            }, status=status.HTTP_404_NOT_FOUND)

        order_data = OrderResource(order).data
        return Response({
            'success': True,
            'order': order_data,
        }, status=status.HTTP_200_OK)


class UpdateOrderStatusView(APIView):
    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Order not found',
            }, status=status.HTTP_404_NOT_FOUND)

        order.status = request.data.get('status', order.status)
        order.save()

        order_data = OrderResource(order).data
        return Response({
            'success': True,
            'message': 'Order status updated',
            'order': order_data,
        }, status=status.HTTP_200_OK)


class DeleteOrderView(APIView):
    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Order not found',
            }, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({
            'success': True,
            'message': 'Order deleted successfully',
        }, status=status.HTTP_200_OK)



class AddShippingToOrderView(APIView):
    def post(self, request,shipping_id,order_number):

        user = request.user

        order = Order.objects.filter(user=user,order_number=order_number).first()

        # به‌روزرسانی فیلد shipping_method_id روی نمونه order
        order.shipping_method_id = shipping_id
        order.save()
        order.refresh_from_db()
        print(f"Shipping method ID after save: {order.shipping_method_id}")

        order_data = OrderResource(order).data
        return Response({
            'success': True,
            'orders': order_data,
        }, status=status.HTTP_200_OK)
