from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductsListView.as_view(), name='products-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='products-detail'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('offers/', OfferListView.as_view(), name='offers-list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
     
]




# urlpatterns = format_suffix_patterns(urlpatterns)
