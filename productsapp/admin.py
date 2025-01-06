from django.contrib import admin
from .models import Product, Cart, CartItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created', 'updated') 
    search_fields = ('name',)  
    list_filter = ('created', 'updated') 
    ordering = ('-created',)  


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')  
    search_fields = ('user__username',) 
    ordering = ('-created',) 


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity') 
    search_fields = ('cart__user__username', 'product__name')  
    list_filter = ('cart__created',)  


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
