from rest_framework import viewsets
from onlineshopApp.models import Product
from onlineshopApp.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer