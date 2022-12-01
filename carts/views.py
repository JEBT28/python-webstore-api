# from django.shortcuts import render
# from carts import models
# from utils import get_or_create_cart

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart
from productos.models import Producto
from .serializers import CartModelSerializer, CartRegisterSerializer, CartUpdateSerializer, CartDeleteSerializer
# Create your views here.
#crear y obtener un carrito de compras


# def cart(request):
#     cart = get_or_create_cart(request)
#     return render(request, 'carts/cart.html',{
#     })

class CartViewSet(viewsets.ModelViewSet):
    permissions = [AllowAny]
    queryset = Cart.objects.all().select_related('id_product')
    serializer_class = CartModelSerializer
    
    @action(methods=['get'], detail=False, url_path='get-cart')
    def userCart(self, request):
        cart = CartModelSerializer(self.get_queryset().filter(id_user=request.user.id),many=True).data
        if not cart:
            return Response({'detail':'No existe productos en el carrito'},status=status.HTTP_200_OK)
        res = {
            'results': cart
        }
        return Response(res, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False, url_path='nuevo')
    def addItem(self, request):
        permissions = [IsAuthenticated]
        id_user = request.user.id
        if not id_user:
            return Response({'detail':'No existe el usuario'},status=status.HTTP_404_NOT_FOUND)
        product = Producto.objects.get(id=request.data['id_product'])
        cost = product.price * request.data['quantity']
        product.stock -= request.data['quantity']
        product.save()
        newItem = {
            'id_user': id_user,
            'id_product': request.data['id_product'],
            'quantity': request.data['quantity'],
            'cost': cost
        }
        serializer = CartRegisterSerializer(data=newItem)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        res = {
            'item': CartModelSerializer(item).data
        }
        return Response(res, status=status.HTTP_201_CREATED)
    
    @action(methods=['put'], detail=False, url_path='incrementItem/(?P<pk>[^/.]+)')
    def incrementItem(self, request, pk):
        instance = self.get_queryset().get(id=pk)
        instance.quantity += 1
        instance.cost = instance.quantity * instance.id_product.price
        product = Producto.objects.get(id=instance.id_product.id)
        product.stock -= 1
        product.save()
        serializer = CartUpdateSerializer(instance,data=CartModelSerializer(instance).data)
        serializer.is_valid(raise_exception=True)
        item = serializer.update(instance,CartModelSerializer(instance).data)
        res = {
            'item': CartModelSerializer(item).data
        }
        return Response(res, status=status.HTTP_201_CREATED)
    
    @action(methods=['put'], detail=False, url_path='decrementItem/(?P<pk>[^/.]+)')
    def decrementItem(self, request, pk):
        instance = self.get_queryset().get(id=pk)
        instance.quantity -= 1
        instance.cost = instance.quantity * instance.id_product.price
        product = Producto.objects.get(id=instance.id_product.id)
        product.stock += 1
        product.save()
        serializer = CartUpdateSerializer(instance,data=CartModelSerializer(instance).data)
        serializer.is_valid(raise_exception=True)
        item = serializer.update(instance,CartModelSerializer(instance).data)
        res = {
            'item': CartModelSerializer(item).data
        }
        return Response(res, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=False, url_path='deleteItem/(?P<pk>[^/.]+)')
    def deleteItem(self, request, pk):
        instance = self.get_queryset().get(id=pk)
        product = Producto.objects.get(id=instance.id_product.id)
        product.stock += instance.quantity
        product.save()
        serializer = CartDeleteSerializer(instance=instance,data = CartModelSerializer(instance).data)
        serializer.is_valid(raise_exception=True)
        item = serializer.delete(instance)
        res = {
            'detail': 'Item eliminado',
            'product': CartModelSerializer(item).data
        }
        return Response(res, status=status.HTTP_200_OK)
    
    @action(methods=['delete'], detail=False, url_path='clearCart')
    def clearCart(self, request):
        id_user = request.user.id
        if not id_user:
            return Response({'detail':'No existe el usuario'},status=status.HTTP_404_NOT_FOUND)
        cart = Cart.objects.filter(id_user=id_user)
        for item in cart:
            product = Producto.objects.get(id=item.id_product.id)
            product.stock += item.quantity
            product.save() 
        cart.delete()
        res = {
            'detail': 'Carrito vaciado'
        }
        return Response(res, status=status.HTTP_200_OK)