from django.shortcuts import render,redirect
from app1.models import Product,Order,Cart,CartItem,Ordered_items
from app1.forms import Orderform,Signup_form,Login_form,SearchForm
from django.contrib.auth import authenticate,login

from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from .forms import CartForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as auth_logout






# Create your views here.
def home(request):
    products=Product.objects.all()
    return render(request,'app1/home.html',{'products':products})


def add_order(request):
    # form=Orderform()
    if request.method=='POST':
        form=Orderform(request.POST)

        if form.is_valid():
            form.save()
            return home(request)
    else:
        form=Orderform()
    return render(request,'app1/order_form.html',{'form':form})



def edit_order(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=='POST':
        form=Orderform(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return home(request)
    else:
        form=Orderform()
       
    return render(request,'app1/order_form.html',{'form':form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'app1/sign_up.html',{'form':form})


def logout(request):
    auth_logout(request)
    return redirect('home')

# def sign_up(request):
#     form=Signup_form()

#     if request.method=='POST':
#         form=Signup_form(request.POST)
#         if form.is_valid():
#             user=form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])
#             form.save(commit=True)
#             login(request,user)
#             return home(request)
#     else:
#         form=Signup_form()
#     return render(request,'app1/sign_up.html',{'form':form})




# def login_page(request):
#     if request.method == 'POST':
#         username=request.POST['username']
#         password=request.POST['password']
#         user=authenticate(request,username=username,password=password)
#         if user is not None:    
#             login(request,user)
#             return home(request)
#         else:
#             pass
#     return render(request,'app1/login.html')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart.total_price
    return render(request, 'app1/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    print(f"Adding product {product_id} to cart...")
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()
    cart.total_price += product.price * cart_item.quantity
    cart.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    cart = Cart.objects.get(user=request.user)
    cart.total_price -= cart_item.product.price * cart_item.quantity
    cart.save()
    return redirect('cart_view')

@login_required
def update_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    form = CartForm(request.POST or None, instance=cart_item)
    if form.is_valid():
        form.save()
        cart = Cart.objects.get(user=request.user)
        cart.total_price = sum([item.product.price * item.quantity for item in CartItem.objects.filter(cart=cart)])
        cart.save()
        return redirect('cart_view')
    return render(request, 'app1/update_cart.html', {'form': form, 'cart_item': cart_item})

# @login_required
# def checkout(request):
#     cart = Cart.objects.get(user=request.user)
#     if cart.total_price > 0:
#         order = Order.objects.create(
#             name=request.user.username,
#             email=request.user.email,
#             address=request.user.profile.address,
#             city=request.user.profile.city,
#             state=request.user.profile.state,
#             zip_code=request.user.profile.zip_code,
#             total_price=cart.total_price
#         )
#         for item in CartItem.objects.filter(cart=cart):
#             order.items.add(item.product)
#         cart.delete()
#         return redirect('order_success')
#     return redirect('cart_view')



# @login_required
# def checkout(request):
#     if request.method == 'POST':
#         # Handle the checkout process (e.g., save order details)
#         return redirect('order_success')
#     # return render(request, 'checkout.html')
#     return render(request, 'app1/order_success.html')

# @login_required
# def checkout(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     total_price = cart.total_price
   
    
#     if request.method == 'POST':
#         # Handle the checkout process (e.g., save order details)
#         form=Orderform(request.POST)
#         if form.is_valid():
#             form.save()
#             # return redirect('checkout')
#     else:
#         form=Orderform()
#     return render(request, 'app1/final_page.html',{'all_items':cart_items,"total_price":total_price},{'form':form})


# @login_required
# def checkout(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     total_price = cart.total_price
    
#     if request.method == 'POST':
#         # Handle the checkout process (e.g., save order details)
#         form = Orderform(request.POST)
#         if form.is_valid():
#             form.save()
#             # return redirect('checkout')
#             # Optionally, redirect after successful form submission
#             # return redirect('order_success')
#     else:
#         form = Orderform()

#     context = {
#         'all_items': cart_items,
#         'total_price': total_price,
#         'form': form,
#     }

#     return render(request, 'app1/final_page.html', context)


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart.total_price
    # ordered=Ordered_items()
    # ordered.ordered_price=total_price
    
    form_data = None
    
    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data  # Capture the cleaned data from the form
            form.save()
             
            # cart_items.delete()
            # cart.total_price=0
            # cart.save()
            
    else:
        form = Orderform()

    context = {
        'all_items': cart_items,
        'total_price': total_price,
        'form': form,
        'form_data': form_data,  # Pass the form data to the template
    }
   

    return render(request, 'app1/final_page.html', context)

def clear_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    cart_items.delete()
    cart.total_price=0
    cart.save()
    return redirect('home')

def All_orders(request):
    orders = Order.objects.all()





# @login_required
# def checkout(request):
#     cart_items = OrderItem.objects.filter()
    
#     if not cart_items:
#         return redirect('cart')  # Redirect to cart if empty

#     if request.method == 'POST':
#         form = CheckoutForm(request.POST)
#         if form.is_valid():
#             # Process the checkout
#             # For example, create an order, deduct inventory, etc.
#             return redirect('success')  # Redirect to a success page
#     else:
#         form = CheckoutForm()

#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#     return render(request, 'shop/checkout.html', {
#         'cart_items': cart_items,
#         'total_price': total_price,
#         'form': form
#     })




# def order_success(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     total_price = cart.total_price
    
#     if request.method == 'POST':
#         # Handle the checkout process (e.g., save order details)
#         form=Orderform(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('order_success')
#     else:
#         form=Orderform()
#     # all_items=CartItem.objects.filter()
#     # cart=Cart()
#     # total_price=cart.total_price
#     return render(request, 'app1/order_success.html',{'all_items':cart_items,"total_price":total_price},{'form':form})




# def product_list(request):
#     form = ProductSearchForm(request.GET or None)
#     products = Product.objects.all()

#     if form.is_valid():
#         query = form.cleaned_data.get('query')
#         category = form.cleaned_data.get('category')

#         if query:
#             products = products.filter(product_name__icontains=query)
#         if category:
#             products = products.filter(category=category)
    
#     context = {
#         'products': products,
#         'form': form,
#     }
#     return render(request, 'product_list.html', context)

# def search_view(request):
#     form=SearchForm(request.GET or None)
#     products=Product.objects.all()

#     if form.is_valid():
#         query=form.cleaned_data.get('query')
#         category=form.cleaned_data.get('category')

#         if query:
#             products=products.filter(product_name__icontains=query)
#         if category:
#             products=products.filter(category=category)
#         content={
#             'products':products,
#             'form':form,
#         }

#     return render(request,'app1/product_list.html',content)




# views.py

def search_view(request):
    form = SearchForm(request.GET or None)
    products = Product.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')

        if query:
            products = products.filter(product_name__icontains=query)
        if category:
            products = products.filter(category=category)

      
        content = {
            'products': products,
            'form': form,
        }
    else:
        
        content = {
            'products': products, 
            'form': form,
        }
    
    # Ensure you return a response
    return render(request, 'app1/product_list.html', content)

    


