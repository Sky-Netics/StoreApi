from rest_framework import serializers
from products.models import Product


class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Product
        fields = "__all__"
       




