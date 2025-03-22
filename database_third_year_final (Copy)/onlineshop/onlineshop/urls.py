from django.contrib import admin
from django.urls import path
from onlineshopApp.views import (
    CountryListView, CityListView, DistrictListView, PostcodeListView,
    UserRegistrationView, ProductListView, CreateOrderView,register_admin, home, products,admin_page
)

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page
    path('products/', products, name='products'),  # Products page
    path('api/countries/', CountryListView.as_view(), name='country-list'),
    path('api/cities/<int:country_id>/', CityListView.as_view(), name='city-list'),
    path('api/districts/<int:city_id>/', DistrictListView.as_view(), name='district-list'),
    path('api/postcodes/<int:district_id>/', PostcodeListView.as_view(), name='postcode-list'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('api/create-order/', CreateOrderView.as_view(), name='create-order'),
    path('api/register-admin/', register_admin, name='register_admin'),
    path('adminss/', admin_page, name='admin_page'), 
]