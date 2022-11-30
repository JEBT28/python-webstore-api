from rest_framework import serializers
from .models import Order, orderDetail
from django.contrib.auth.models import User
from productos.serializers import ProductModelSerializer
class OrderDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = orderDetail
        fields = (
            'id',
            'order',
            'quantity',
            'cost',
            'product',
        )
    product = ProductModelSerializer()
class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'total',
            'direction',
            'date',
            'orderDetails'
        )
    orderDetails = OrderDetailModelSerializer(many=True)


class OrderRegisterSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    total = serializers.FloatField()
    direction = serializers.CharField(max_length=100)
    def validate(self, data):
        if data['total'] < 0:
            raise serializers.ValidationError('El total no puede ser negativo')
        return data

    def create(self, data):
        order = Order.objects.create(**data)
        return order

class OrderDeleteSerializer(serializers.Serializer):
    def delete(self,instance):
        instance.delete()
        return instance

