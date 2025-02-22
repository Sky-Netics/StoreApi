from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from usercart import models
from usercart.api.serializers import *
from products.models import Product
from usercart.models import Cart, CartItem
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema



class CartView(APIView):
    
    def get(self, request):
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, product_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            product = Product.objects.get(id=product_id)
            quantity = request.data.get('quantity', 1)  # Default to 1 if not provided
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item = cart.add_items(product, quantity=request.data.get('quantity', 1))

        return Response({
            "message": "Item added to cart successfully",
            "product_name": cart_item.product.name,
            "quantity": cart_item.quantity,
            "total_price": cart_item.get_total_price(),
            "cart_total_price": cart.get_total_price()
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CartItemQuantitySerializer)
    def patch(self, request,product_id):

        # Get the user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the cart item to update
        try:
            cart_item = CartItem.objects.get(id=product_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response({"message": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        # Pass the cart item and the updated quantity to the serializer
        serializer = CartItemQuantitySerializer(cart_item, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    



class RemoveFromCartView(APIView):
    
    @swagger_auto_schema(operation_description="Remove a product from the user's cart.")
    def delete(self, request, product_id, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"message": "Item not in cart"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)


class UpdateQuantityView(APIView):
  
    @swagger_auto_schema(
        operation_description="Update the quantity of an item in the user's cart.",
        request_body=CartItemSerializer
    )
    def patch(self, request, product_id, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"message": "Item not in cart"}, status=status.HTTP_404_NOT_FOUND)

        # Get new quantity from request data
        quantity = request.data.get('quantity')
        if quantity is None or quantity <= 0:
            return Response({"message": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Item quantity updated successfully"}, status=status.HTTP_200_OK)