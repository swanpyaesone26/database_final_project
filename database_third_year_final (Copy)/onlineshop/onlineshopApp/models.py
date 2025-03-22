# models.py
from django.db import models

class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'countries'

    def __str__(self):
        return self.country_name


class Cities(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    country = models.ForeignKey('Countries', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'cities'

    def __str__(self):
        return self.city_name


class Districts(models.Model):
    district_id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=100)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'districts'

    def __str__(self):
        return self.district_name


class Postcodes(models.Model):
    postcode_id = models.AutoField(primary_key=True)
    postcode = models.CharField(max_length=10)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'postcodes'

    def __str__(self):
        return self.postcode


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    address_line = models.CharField(max_length=255)
    postcode = models.ForeignKey(Postcodes, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'address'

    def __str__(self):
        return self.address_line


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.name


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'categories'

    def __str__(self):
        return self.category_name


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, db_column='category_id')

    class Meta:
        managed = False
        db_table = 'products'

    def __str__(self):
        return self.product_name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return f"Order {self.order_id}"


class OrderItems(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, db_column='order_id')
    product = models.ForeignKey('Products', on_delete=models.CASCADE, db_column='product_id')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'order_items'

    def __str__(self):
        return f"Order Item {self.order_item_id} for Order {self.order_id}"
    
class Admins(models.Model):
    admin_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
    admin_name = models.CharField(max_length=255)  # Admin's name
    admin_email = models.EmailField(unique=True)   # Admin's email (unique)
    admin_password = models.CharField(max_length=255)  # Admin's password (hash this in production!)
    admin_role = models.CharField(
        max_length=20,
        choices=[('superadmin', 'Super Admin'), ('editor', 'Editor'), ('viewer', 'Viewer')]  # Enum-like choices
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation

    class Meta:
        managed = False
        db_table = 'admins'

    def __str__(self):
        return self.admin_name