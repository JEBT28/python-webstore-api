from rest_framework import serializers

from productos.models import Producto
from .models import Cart
from django.contrib.auth.models import User
from productos.serializers import ProductModelSerializer

class CartModelSerializer(serializers.ModelSerializer):
    # id_product = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    # id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Cart
        fields = (
            'id',
            'quantity',
            'cost',
            'id_user',
            'id_product',
        )
    id_product = ProductModelSerializer()

class CartRegisterSerializer(serializers.Serializer):
    id_product = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    quantity = serializers.IntegerField()
    cost =  serializers.FloatField()
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    def validate(self, data):
        if data['quantity'] < 0:
            raise serializers.ValidationError('La cantidad no puede ser negativa')
        if data['cost'] < 0:
            raise serializers.ValidationError('El costo no puede ser negativo')
        return data

    def create(self, data):
        cart = Cart.objects.create(**data)
        return cart

class CartUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(required=False)
    cost =  serializers.FloatField(required=False)

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError('La cantidad no puede menor o igual a 0')
        if data['cost'] < 0:
            raise serializers.ValidationError('El costo no puede ser negativo')
        return data

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.save()
        return instance

class CartDeleteSerializer(serializers.Serializer):
    def delete(self,instance):
        instance.delete()
        return instance
