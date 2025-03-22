# serializers.py
from rest_framework import serializers
from .models import Countries, Cities, Districts, Postcodes, Users, Categories, Products, Orders, OrderItems

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = '__all__'


class PostcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postcodes
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'name', 'email', 'password', 'phone_number', 'address_line', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password in responses
            'address_line': {'required': True},  # Ensure address_line is required
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category_id', 'category_name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['product_id', 'product_name', 'description', 'price', 'created_at', 'category']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)  # Nested serializer for order items

    class Meta:
        model = Orders
        fields = ['payment_method', 'total_price', 'items']  # Removed 'user' since we're allowing anonymous orders

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # Extract order items
        order = Orders.objects.create(**validated_data)  # Create the order
        for item_data in items_data:
            OrderItems.objects.create(order=order, **item_data)  # Create order items
        return order