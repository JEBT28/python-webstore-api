from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from cloudinary.uploader import upload, destroy

from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import ProductModelSerializer, ProductRegisterSerializer, ProductUpdateSerializer, ProductDeleteSerializer
from .models import Producto

class ProductViewSet(viewsets.ModelViewSet):
    permisions = [AllowAny]
    queryset = Producto.objects.all()
    serializer_class = ProductModelSerializer
    
    @action(detail=False, methods=['get'])
    def todos(self,request):
        
        products = ProductModelSerializer(self.get_queryset(), many=True).data
        
        res = {
            'results': products
        }
        
        return Response(res, status=status.HTTP_200_OK)
        
    # @action(detail=False, methods=['get'])
    # def id(self, request, pk):
    #     product = ProductModelSerializer(self.get_queryset().get(id=pk)).data
        
    #     if not product:
    #         return Response({'detail':'No existe el producto'},status=status.http_404_NOT_FOUND)
        
    #     res = {
    #         'results': product
    #     }

    #     return Response(res, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def nuevo(self, request):
        b64_img = request.data['img'] or None
        
        if b64_img:
            img_url = upload(b64_img)['url']

        request.data['img_url'] = img_url or ''

        serializer = ProductRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        res = {
            'product': ProductModelSerializer(product).data
        }
        return Response(res, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['put'], url_path='editar/(?P<pk>[^/.]+)')
    def editar(self, request, pk):
        instance = self.get_queryset().get(id=pk)
        if not instance:
            return Response({'detail':'No existe el producto'},status=status.http_404_NOT_FOUND)
        
        print(request.data.get('description'))
        serializer = ProductUpdateSerializer(instance = instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.update(instance, serializer.validated_data)
        res = {
            'product': ProductModelSerializer(product).data
        }
        return Response(res, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'], url_path='eliminar/(?P<pk>[^/.]+)')
    def eliminar(self, request, pk):
        instance = self.get_queryset().get(id=pk)
        img_url = instance.img_url
        if not instance:
            return Response({'detail':'No existe el producto'},status=status.http_404_NOT_FOUND)
        
        serializer = ProductDeleteSerializer(instance = instance,data=ProductModelSerializer(instance).data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        
        if img_url:
            destroy(img_url)
        
        res = {
            'product': ProductModelSerializer(product).data
        }

        return Response(res, status=status.HTTP_200_OK)
    