from django.contrib import admin
from app1.models import Product,Order,Cart,CartItem

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
