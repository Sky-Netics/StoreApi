from django.contrib import admin
from .models import  Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')  
    search_fields = ('user__username',) 
    ordering = ('-created',) 


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity') 
    search_fields = ('cart__user__username', 'product__name')  
    list_filter = ('cart__created',)  



admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)