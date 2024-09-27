from django.contrib import admin
from app1.models import Product,Order,Cart,CartItem,OrderDetails,Comments,Ratings,OrderDetails1,OrderedItems2

# Register your models here.

class OrderedItems2Admin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total_price', 'status')
    list_editable = ('status',)  # Allow admins to change the status in the list view

admin.site.register(OrderedItems2, OrderedItems2Admin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderDetails)
admin.site.register(Comments)
admin.site.register(Ratings)



