"""
URL configuration for pro_ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app1.views import home,add_order,edit_order,signup,logout,search_view
from app1.views import cart_view,add_to_cart,update_cart,remove_from_cart,checkout,clear_cart
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

    
    
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    #  Gayle+333