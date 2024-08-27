
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app1.views import home,add_order,edit_order,signup,logout,search_view,Show_all_orderes,rate_product
from app1.views import cart_view,add_to_cart,update_cart,remove_from_cart,checkout,clear_cart,view_product,add_comment,edit_comment,delete_comment,all_comment
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('home',home,name='home'),
    path('order/',add_order,name='add_order'),
    path('order<int:pk>/',edit_order,name='edit_order'),
    

    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(template_name='app1/login.html'), name='login'),
    path('logout/', logout, name='logout'),

    path('cart/', cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    # path('order_success/', order_success, name='order_success'),
    
    path('search',search_view,name='search_view'),
    path('clear_cart',clear_cart,name='clear_cart'),
    path('Show_all_orderes',Show_all_orderes,name='Show_all_orderes'),
    path('view_product/<int:product_id>/',view_product,name='view_product'),
    path('all_comment/<int:product_id>/',all_comment,name='all_comment'),

    path('add_comment/<int:product_id>/',add_comment,name='add_comment'),
    path('edit_comment/<int:pk>/',edit_comment,name='edit_comment'),
    path('delete_comment/<int:pk>/',delete_comment,name='delete_comment'),

    


    path('rate_product/<int:product_id>/',rate_product,name='rate_product'),



    
    
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    #  Gayle+333