from django.urls import path,include
# from carts import views as cart_view
from rest_framework.routers import DefaultRouter
from . import views as cart_views

# app_name = 'carts'

# urlpatterns = [path('',cart_view.cart, name='cart')]

router = DefaultRouter()
router.register(r'carts', cart_views.CartViewSet, basename='carts')

urlpatterns = [
    path('', include(router.urls))
]
