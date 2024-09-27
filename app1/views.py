from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404
from app1.models import Product,Order,Cart,CartItem,Ordered_items,OrderDetails,Comments,Ratings,OrderDetails1,OrderedItems2
from app1.forms import Orderform,Signup_form,Login_form,SearchForm,CommentForm,Ratings_Form
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from .forms import CartForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from datetime import timedelta

def home(request):
    products=Product.objects.all()
    return render(request,'app1/home.html',{'products':products})

def about(request):
    return render(request, 'app1/about.html')

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


def view_product(request,product_id):
    product=Product.objects.get(id=product_id)
    average_rating=product.get_average_ratings()
    rating_range = range(1, 6)  

    context = {
        'product': product,
        'average_rating': average_rating,
        'range': rating_range,  # Pass the range to the template
    }
    # return render(request,'app1/view_product.html',{'product':product})
    return render(request, 'app1/view_product.html', context)


# def all_comment(request):
#     comments=Comments.objects.all()
#     return render(request,'app1/comment.html',{'comments':comments})

def all_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comments.objects.filter(id_com=product)
    form = CommentForm()

    return render(request, 'app1/comment.html', {
        'product': product,
        'comments': comments,
        'form': form
    })
    

def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  
            comment.id_com = product           
            comment.user = request.user       
            comment.save()   
                             
            return redirect('all_comment', product_id=product.id)  
    else:
        form = CommentForm()

    return render(request, 'app1/comment.html', {'form': form, 'product': product})


def edit_comment(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    if request.user != comment.user:
        return HttpResponseForbidden()
    
    product = comment.id_com  
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save() 
            return redirect('all_comment', product_id=product.id)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'product': product,
        'comment': comment
    }
    return render(request, 'app1/comment.html', context)


def delete_comment(request,pk):
    comment=get_object_or_404(Comments,pk=pk)
    product_id=comment.id_com.id
    product = get_object_or_404(Product, id=product_id)
    if request.user!=comment.user:
        return HttpResponseForbidden()
    
    if request.method=="POST":
        comment.delete()
        return redirect('all_comment',product_id=product_id)
    context={
        
        'product':product,
        'comment':comment,
    }
    return render(request,'app1/delete_comment.html',context)


@login_required
def rate_product(request,product_id):
    product=get_object_or_404(Product,id=product_id)
   
    rating = Ratings.objects.filter(product=product, user=request.user).first()

    if request.method=='POST':
        form=Ratings_Form(instance=rating)
        form = Ratings_Form(request.POST, instance=rating)
        if form.is_valid():
            rating=form.save(commit=False)
            
            rating.user = request.user
            rating.product=product
            rating.save()

            return redirect('view_product',product_id=product.id)
    else:
        form=Ratings_Form(instance=rating)
        
    context={
            'product':product,
            'form':form,
            'average_rating':product.get_average_ratings(),
        }

    return render(request,'app1/rate_product.html',context)
    

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


def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart.total_price
    return render(request, 'app1/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# @login_required
# def checkout(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     total_price = cart.total_price
#     form_data = None
    
    
    
#     if request.method == 'POST':
#         form = Orderform(request.POST)
#         if form.is_valid():
           
#             form_data = form.cleaned_data  
#             form.save()
            
#             for item in cart_items:
#                 OrderDetails.objects.create(
#                     user=request.user,
#                     total_price=cart.total_price,
#                     product_name=item.product.product_name,
#                     image=item.product.image,
#                     quantity=item.quantity,
#                     price=item.product.price,  
#                     )  
#     else:
#         form = Orderform()

#     context = {
#         'all_items': cart_items,
#         'total_price': total_price,
#         'form': form,
#         'form_data': form_data,  
#     }
   

#     return render(request, 'app1/final_page.html', context)


@login_required
def order_success(request):
    return render(request, 'app1/order_success2.html')






@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart.total_price

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add some items before checking out.")
        return redirect('cart_view')

    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Prepare items for the order
                items = [
                    {
                        'product_name': item.product.product_name,
                        'quantity': item.quantity,
                        'price': item.product.price
                    }
                    for item in cart_items
                ]

                # Ensure items are not empty
                if not items:
                    messages.error(request, "There are no items to order.")
                    return redirect('cart_view')

                # Create a new Order
                order = OrderedItems2(
                    user=request.user,
                    total_price=total_price
                )

                # Set the items for the order before saving
                order.set_items(items)
                order.save()

                # Clear the cart
                cart_items.delete()
                cart.total_price = 0
                cart.save()

            messages.success(request, "Your order has been placed successfully!")
            return redirect('order_success')
        else:
            messages.error(request, "There was an error with your order. Please check the form and try again.")
    else:
        form = Orderform()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    }

    return render(request, 'app1/final_page.html', context)





# def order_history(request):
#     # Fetch only the orders for the logged-in user
#     orders = OrderedItems2.objects.filter(user=request.user)
#     return render(request, 'app1/order_history.html', {'orders': orders})

def order_history(request):
    orders = OrderedItems2.objects.filter(user=request.user)
    for order in orders:
        order.order_date = order.order_date + timedelta(hours=5, minutes=30)  # Adjust to IST
    return render(request, 'app1/order_history.html', {'orders': orders})


def Show_all_orderes(request): 
    orders = OrderDetails.objects.filter(user=request.user)
    return render (request,'app1/show_order.html',{'orders':orders})


def clear_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    cart_items.delete()
    cart.total_price=0
    cart.save()
    return redirect('home')

def All_orders(request):
    orders = Order.objects.all()

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

    


