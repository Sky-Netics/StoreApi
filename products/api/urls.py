from django.urls import path
from .views import ProductsListView, ProductDetailView, ProductSearchView



urlpatterns = [
    path('products/', ProductsListView.as_view(), name='products-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='products-detail'),
     path('products/search/', ProductSearchView.as_view(), name='product-search'),
]




# urlpatterns = format_suffix_patterns(urlpatterns)
