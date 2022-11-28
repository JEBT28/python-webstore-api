from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from carts.models import Cart
from django.contrib.auth.models import User
from orders.serializers import OrderModelSerializer, OrderRegisterSerializer, OrderDeleteSerializer
from .models import Order,orderDetail
from django.db.models import Sum
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    permissions = [IsAuthenticated]
    queryset = Order.objects.all().prefetch_related('orderDetails')
    serializer_class = OrderModelSerializer
    
    @action(detail=False, methods=['get'], url_path='historial')
    def ordersByUser(self, request):
        permissions = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response({'detail': 'No autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
 
        orders = OrderModelSerializer(self.get_queryset().filter(user=request.user), many=True).data
        res = {
            'results': orders
        } 
        return Response(res, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'],url_path='createOrder')
    def newOrder(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'No autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
        itemsInCart = Cart.objects.filter(id_user=request.user.id)
        if len(itemsInCart) == 0:
            return Response({'detail': 'No hay productos en el carrito'}, status=status.HTTP_200_OK)
        total = itemsInCart.aggregate(Sum('cost'))['cost__sum']
        print(total)
        order = {
            "user": User.objects.get(id=request.user.id).id,
            "total": total,
            'direction': request.data['direction']
        }
        serializer = OrderRegisterSerializer(data=order)
        serializer.is_valid(raise_exception=True)
        
        order = serializer.save()
        
        for item in itemsInCart:
            od = orderDetail.objects.create(order=order, product=item.id_product, quantity=item.quantity, cost=item.cost)
            od.save()
        res = {
            'order': OrderModelSerializer(order).data
        }
        itemsInCart.delete()
        return Response(res, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['delete'], url_path='delete/(?P<pk>[^/.]+)')
    def deleteOrder(self,request,pk):
        instance = self.get_queryset().get(id=pk)
        serializer = OrderDeleteSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.delete(instance)
        res = {
            'detail': 'Orden eliminada'
        }
        return Response(res, status=status.HTTP_200_OK)