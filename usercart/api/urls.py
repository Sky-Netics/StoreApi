from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView



urlpatterns = [
   
    path('cart/', CartView.as_view(), name='cart_view'), 
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),  
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'), 
]




# urlpatterns = format_suffix_patterns(urlpatterns)
