from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from orders.models.order import Order

from orders.serializers.orderresource import OrderResource


class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request):

        user = request.user
        orders = Order.objects.filter(user=user).prefetch_related('details__product')
        orders_data = OrderResource(orders, many=True).data
        return Response({'orders': orders_data}, status=status.HTTP_200_OK)
