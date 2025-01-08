from django.urls import path
from .views import ProductsListView, ProductDetailView



urlpatterns = [
    path('products/', ProductsListView.as_view(), name='products-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='products-detail'),
]




# urlpatterns = format_suffix_patterns(urlpatterns)
