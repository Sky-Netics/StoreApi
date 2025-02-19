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
    image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    url = models.URLField(blank=True)
    def __str__(self):
        return self.name



#python .\manage.py makemigrations



    