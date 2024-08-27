from django.db import models

# Create your models here.
class Product(models.Model):
    id=models.IntegerField(primary_key=True)
    product_name=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount_price=models.IntegerField()
    cat=[('acc','Accessories'),('sports','Sports'),('bag','Bag'),('food','food'),('default','Default')]
    category=models.CharField(max_length=100,choices=cat)
    image=models.ImageField()
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.id)+' '+self.product_name


class Order(models.Model):
    
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField()
   
    # total_price = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name 
    

class Ordered_items(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    ordered_product=models.ForeignKey(Product,on_delete=models.CASCADE)
    ordered_quan=models.PositiveIntegerField()
    ordered_price=models.DecimalField(max_digits=20,decimal_places=2)


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} : name :{self.product_name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"