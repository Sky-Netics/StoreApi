from django.urls import path
from .views import *



urlpatterns = [
    # path('orders/', OrderListView.as_view(), name='order-list'),
    path('userorder/', CreateOrderView.as_view(), name='orders-detail'),
]




# urlpatterns = format_suffix_patterns(urlpatterns)
