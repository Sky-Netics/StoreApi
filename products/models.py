from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/images/')
    url = models.URLField(blank=True)
    def __str__(self):
        return self.name



#python .\manage.py makemigrations


# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
#     created = models.DateTimeField(default=now)
#     updated = models.DateTimeField(auto_now=True)
#     products = models.ManyToManyField(Product, through='CartItem', related_name='carts')
#     def __str__(self):
#         return f"Cart of {self.user.username}"


#     def get_total_price(self):
        
#         total = 0
#         for item in self.items.all():
#             total += item.get_total_price()
#         return total

#     def item_count(self):
#         """ Returns the number of items in the cart """
#         return sum(item.quantity for item in self.items.all())


#     def add_items(self, product, quantity=1):
#         """
#         Add a product to the cart or update the quantity if it already exists in the cart.
#         If the product is not in the cart, it is added; if it is already present, the quantity is updated.
#         """
#         # Ensure `product` is a valid Product instance
#         if not isinstance(product, Product):
#             raise ValueError("The provided product is not a valid Product instance.")
        
#         # Check if the product already exists in the cart
#         cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)

#         if not created:
#             # If the product already exists in the cart, just update the quantity
#             cart_item.quantity += quantity
#             cart_item.save()

#         return cart_item
        
        
       

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name="cart_items", on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} of {self.product.name}"

#     def get_total_price(self):
       
#         return self.product.price * self.quantity

    
    