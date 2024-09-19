from app1.models import Order,Cart,CartItem
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Orderform(forms.ModelForm):
   
    class Meta:
        model=Order
        fields='__all__'

class Signup_form(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=('username','email','password1','password2')

class Login_form(UserCreationForm):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)



class CartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('quantity',)
    

        
# class ProductSearchForm(forms.Form):
#     query = forms.CharField(max_length=255, required=False, label='Search')
#     category = forms.ChoiceField(choices=[
#         ('', 'All Categories'),
#         ('acc', 'Accessories'),
#         ('sports', 'Sports'),
#         ('bag', 'Bag'),
#         ('food', 'Food'),
#         ('default', 'Default')
#     ], required=False)


class SearchForm(forms.Form):
    query=forms.CharField(max_length=255,required=False,label='Search')
    category=forms.ChoiceField(choices=[
        ('', 'All Categories'),
        ('acc', 'Accessories'),
        ('sports', 'Sports'),
        ('bag', 'Bag'),
        ('food', 'Food'),
        ('default', 'Default')
        ],required=False)
    