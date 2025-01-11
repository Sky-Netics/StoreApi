from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from orders import models
from orders.api.serializers import *
from usercart.api.serializers import Cart
from orders.models import Order
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema





# class OrderListView(APIView):
#     # permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

#     def get(self, request):

#         orders = Order.objects.filter(user=request.user)

#         if not orders.exists():
#             return Response({"message": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = OrderSerializer(orders, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class OrderListView(APIView):
#     def get(self, request):
#         orders = Order.objects.all()
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()  
            return Response({
                "message": "Order created successfully",
                "order": OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)