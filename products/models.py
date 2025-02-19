from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    off = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  
    # offers = models.ManyToManyField(Offer, blank=True, related_name="products")  
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    url = models.URLField(blank=True)
    def __str__(self):
        return self.name

    def get_final_price(self):

        # max_offer_discount = self.offers.aggregate(models.Max('discount_percentage'))['discount_percentage__max'] or 0
        # total_discount = max(self.off, max_offer_discount)  # بیشترین تخفیف را اعمال کن
        return self.price - (self.price * self.off / 100)



#python .\manage.py makemigrations



    