from rest_framework import serializers
from orders.models import Order
from usercart.models import *
from usercart.api.serializers import *
from usercart.api.views import *




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_last_name', 'phone_number',
            'address', 'postal_code', 'payment_method',
            'notes', 'total_price'  
        ]
        read_only_fields = ['total_price']  
       

    def create(self, validated_data):
        user = self.context['request'].user 

        
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("The cart is empty or does not exist.")

        
        cart_items = cart.items.all()
        if not cart_items.exists():
            raise serializers.ValidationError("Your cart is empty.")

       
        total_price = cart.get_total_price()

        
        order = Order.objects.create(user=user, total_price=total_price, **validated_data)

        cart_items.delete()

        return order
