from rest_framework import serializers
from usercart.models import Cart, CartItem





class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id', 'product_name', 'product_price', 'product_image', 'quantity', 'get_total_price']



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created', 'updated', 'items', 'get_total_price', 'item_count']

class CartItemQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

