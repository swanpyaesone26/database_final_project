# views.py
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Countries, Cities, Districts, Postcodes, Users, Categories, Products, Orders, OrderItems
from .serializers import (
    UserSerializer, CountrySerializer, CitySerializer, DistrictSerializer,
    PostcodeSerializer, CategorySerializer, ProductSerializer, OrderSerializer
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Admins  # Import the Admins model
import json

def home(request):
    return render(request, 'home.html')

def admin_page(request):
    return render(request, 'admin.html')


def products(request):
    return render(request, 'products.html')


class UserRegistrationView(APIView):
    def post(self, request):
        print('Received data:', request.data)  # Log the received data

        # Extract data from the request
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        address = request.data.get('address')  # User input for address
        country_id = request.data.get('country')
        city_id = request.data.get('city')
        district_id = request.data.get('district')
        postcode_id = request.data.get('postcode')

        # Fetch the selected country, city, district, and postcode
        try:
            country = Countries.objects.get(country_id=country_id)
            city = Cities.objects.get(city_id=city_id)
            district = Districts.objects.get(district_id=district_id)
            postcode = Postcodes.objects.get(postcode_id=postcode_id)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Combine the address fields into a single string
        address_line = f"{address}, {district.district_name}, {city.city_name}, {country.country_name}, {postcode.postcode}"

        # Prepare the user data
        user_data = {
            'name': name,
            'email': email,
            'password': password,
            'phone_number': phone_number,
            'address_line': address_line,  # Combined address saved in the 'address_line' field
        }

        # Save the user data
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('Serializer errors:', serializer.errors)  # Log serializer errors
        print('User data:', user_data)  # Log user data for debugging
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryListView(APIView):
    def get(self, request):
        countries = Countries.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)


class CityListView(APIView):
    def get(self, request, country_id):
        cities = Cities.objects.filter(country_id=country_id)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class DistrictListView(APIView):
    def get(self, request, city_id):
        districts = Districts.objects.filter(city_id=city_id)
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)


class PostcodeListView(APIView):
    def get(self, request, district_id):
        postcodes = Postcodes.objects.filter(district_id=district_id)
        serializer = PostcodeSerializer(postcodes, many=True)
        return Response(serializer.data)

class ProductListView(APIView):
    def get(self, request):
        # Fetch all categories
        categories = Categories.objects.all()

        # Prepare the response data
        data = []
        for category in categories:
            # Fetch products for the current category
            products = Products.objects.filter(category=category)
            product_serializer = ProductSerializer(products, many=True)

            # Serialize the current category
            category_serializer = CategorySerializer(category)

            # Append the category and its products to the response data
            data.append({
                'category': category_serializer.data,
                'products': product_serializer.data
            })

        return Response(data)
''''
class ProductListView(APIView):
    def get(self, request):
        # Fetch all categories
        categories = Categories.objects.all()
        category_serializer = CategorySerializer(categories, many=True)

        # Fetch products for each category
        data = []
        for category in categories:
            products = Products.objects.filter(category=category)
            product_serializer = ProductSerializer(products, many=True)
            data.append({
                'category': category_serializer.data,
                'products': product_serializer.data
            })

        return Response(data)'''''


class CreateOrderView(APIView):
    def post(self, request):
        # Extract data from the request
        payment_method = request.data.get('payment_method')
        total_price = request.data.get('total_price')
        cart_items = request.data.get('cart_items')  # List of products in the cart

        # Create the order
        order = Orders.objects.create(
            payment_method=payment_method,
            total_price=total_price
        )

        # Create order items and fetch product names
        items = []
        for item in cart_items:
            product = Products.objects.get(product_id=item['product_id'])
            OrderItems.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )
            items.append({
                'product_name': product.product_name,
                'quantity': item['quantity'],
                'price': item['price']
            })

        # Generate the voucher
        voucher = {
            'order_id': order.order_id,
            'created_time': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'total_price': float(order.total_price),  # Convert Decimal to float for JSON serialization
            'items': items
        }

        # Return the voucher in the response
        return Response({'message': 'Order created successfully!', 'voucher': voucher}, status=status.HTTP_201_CREATED)
    
@csrf_exempt
def register_admin(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)

            # Create a new admin
            admin = Admins(
                admin_name=data['admin_name'],
                admin_email=data['admin_email'],
                admin_password=data['admin_password'],  # Note: Hash the password in production!
                admin_role=data['admin_role']
            )
            admin.save()  # Save the admin to the database

            # Return success response
            return JsonResponse({'success': True, 'message': 'Admin registered successfully!'})
        except Exception as e:
            # Return error response
            return JsonResponse({'success': False, 'message': str(e)})
    # Return error for invalid request method
    return JsonResponse({'success': False, 'message': 'Invalid request method'})