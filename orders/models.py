from django.db import models
from usercart.models import Cart, CartItem
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders') 
    customer_name = models.CharField(max_length=100)
    customer_last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='credit_card')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    notes = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


    