from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from products.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Product, through='CartItem', related_name='carts')
    def __str__(self):
        return f"Cart of {self.user.username}"


    def get_total_price(self):
        
        total = 0
        for item in self.items.all():
            total += item.get_total_price()
        return total

    def item_count(self):
        
        return sum(item.quantity for item in self.items.all())


    def add_items(self, product, quantity=1):
       
     
        if not isinstance(product, Product):
            raise ValueError("The provided product is not a valid Product instance.")
        
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item
        
        
       

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
       
        return self.product.price * self.quantity