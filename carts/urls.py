from django.urls import path
from carts import views as cart_view
app_name = 'carts'

urlpatterns = [path('',cart_view.cart, name='cart')]