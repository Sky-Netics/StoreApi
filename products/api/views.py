from rest_framework.decorators import api_view
from fuzzywuzzy import fuzz
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from products import models
from products.api.serializers import *
from products.models import Product
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.postgres.search import TrigramSimilarity

class ProductsListView(APIView):
    # authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductsSerializer(many=True))
    def post(self, request, format=None):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProductsSerializer(many=True))
    def put(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProductsSerializer(many=True))
    def delete(self, request):
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductsSerializer(product)
        return Response(serializer.data)


    @swagger_auto_schema(request_body=ProductsSerializer(many=True))
    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProductsSerializer(many=True))
    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class ProductSearchView(APIView):

  
    @swagger_auto_schema(
        operation_description="Search products by name",
        responses={
            200: ProductsSerializer(many=True),
            404: 'No product found with the given name'
        },
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY, description="Search by product name", type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        name = request.query_params.get('name', None)

        if not name:
            return Response({"error": "Please provide a 'name' query parameter"}, status=status.HTTP_400_BAD_REQUEST)

        name = name.strip().lower()

        products = Product.objects.all()
        matched_products = [
            product for product in products
            if fuzz.partial_ratio(product.name.lower(), name) > 80  
        ]

        if not matched_products:
            return Response({"error": "No product found with the given name"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductsSerializer(matched_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
