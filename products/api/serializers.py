from rest_framework import serializers
from products.models import *

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

        
class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    final_price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = "__all__"
       
    def get_final_price(self, obj):
        return obj.get_final_price()



