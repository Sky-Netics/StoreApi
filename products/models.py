from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.

class Offer(models.Model):
    title = models.CharField(max_length=50)  # عنوان تخفیف (مثلاً یلدای شگفت‌انگیز)
    description = models.TextField(blank=True)  # توضیحات بیشتر درباره تخفیف
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  # درصد تخفیف
    start_date = models.DateTimeField()  # تاریخ شروع تخفیف
    end_date = models.DateTimeField()  # تاریخ پایان تخفیف
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.discount_percentage}%"

    def is_active(self):
        """ بررسی می‌کند که تخفیف هنوز معتبر است یا نه """
        now = timezone.now()
        return self.start_date <= now <= self.end_date

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
    offers = models.ManyToManyField(Offer, blank=True, related_name="products")  
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    url = models.URLField(blank=True)
    def __str__(self):
        return self.name

    def get_final_price(self):
    
        active_offers = self.offers.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
        max_offer_discount = active_offers.aggregate(models.Max('discount_percentage'))['discount_percentage__max'] or 0

        total_discount = max(self.off, max_offer_discount)

        return self.price - (self.price * total_discount / 100)


#python .\manage.py makemigrations



    