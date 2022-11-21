from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated, AllowAny

# Serializers
from users.serializers import UserLoginSerializer, UserModelSerializer, UserRegisterSerializer, UserEditSerializer, UserChangesPasswordSerializer

class UserViewSet(viewsets.GenericViewSet):
    permisions = [AllowAny]
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        res = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(res,status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        permisions = [IsAuthenticated]

        if not request.user:
            return Response({'detail':'No autenticado'},status=status.HTTP_401_UNAUTHORIZED)

        request.user.auth_token.delete()
        res = {
            'msg': 'Cierre de sesion exitoso'
        }
        return Response(res, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        permisions = [IsAuthenticated]

        if not request.user.is_authenticated:
            return Response({'detail':'No autenticado'},status=status.HTTP_401_UNAUTHORIZED)

        res = {
            'user': UserModelSerializer(request.user).data,
        }
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def todos(self,request):
        permisions = [IsAuthenticated]

        if not request.user.is_authenticated:
            return Response({'detail':'No autenticado'},status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response({'detail':'No tiene permisos para realizar la accion'},status=status.HTTP_400_BAD_REQUEST)

        users = UserModelSerializer(self.queryset, many=True).data

        res ={
            'users': users
        }

        return Response(res, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def nuevo(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail':'Usuario creado exitosamente'},status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['put'])
    def actualizar(self,request):
        permisions = [IsAuthenticated]

        if not request.user.is_authenticated:
            return Response({'detail':'No autenticado'},status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserEditSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        res = {
            'msg':'Usuario actualizado exitosamente'
        }
        
        return Response(res, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['put'])
    def change_password(self,request):
        permisions = [IsAuthenticated]

        if not request.user.is_authenticated:
            return Response({'detail':'No autenticado'},status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserChangesPasswordSerializer(instance=request.user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        res = {
            'msg':'Contraseña actualizada exitosamente'
        }
        
        return Response(res, status=status.HTTP_200_OK)
    