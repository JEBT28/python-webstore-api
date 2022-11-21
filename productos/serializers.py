
from rest_framework import serializers
from .models import Producto

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
            'img_url'
        )
        
class ProductRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    stock = serializers.IntegerField()
    img_url = serializers.CharField(max_length=200)
    
    def validate(self, data):
        
        if data['stock'] < 0:
            raise serializers.ValidationError('El stock no puede ser negativo')
        
        if data['price'] < 0:
            raise serializers.ValidationError('El precio no puede ser negativo')
        
        return data
        
    
    def create(self, data):
        product = Producto.objects.create(**data)
        return product
    
class ProductUpdateSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=50, required=False)
    description = serializers.CharField(max_length=100,required=False)
    stock = serializers.IntegerField(required=False)
    price = serializers.FloatField(required=False)
    img_url = serializers.CharField(max_length=200, required=False)

    def validate(self, data):
        if 'stock' in data and data['stock'] < 0:
            raise serializers.ValidationError('El stock no puede ser negativo')
        
        if 'price' in data and data['price'] < 0:
            raise serializers.ValidationError('El precio no puede ser negativo')
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.price = validated_data.get('price', instance.price)
        instance.img_url = validated_data.get('img_url', instance.img_url)
        instance.save()
        return instance

class ProductDeleteSerializer(serializers.Serializer):
    def update(self, instance,data):
        instance.delete()
        return instance