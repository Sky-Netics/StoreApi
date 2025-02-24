from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   
    path('cart/', CartView.as_view(), name='cart_view'), 
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),  
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'), 
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urlpatterns = format_suffix_patterns(urlpatterns)
