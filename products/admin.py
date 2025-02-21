from django.contrib import admin
from .models import Product, Offer


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created', 'updated') 
    search_fields = ('name',)  
    list_filter = ('created', 'updated') 
    ordering = ('-created',)  

class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('title',)
    list_filter = ('start_date', 'end_date')



admin.site.register(Product, ProductAdmin)
admin.site.register(Offer, OfferAdmin)
