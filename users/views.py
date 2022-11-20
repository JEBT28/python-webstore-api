from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated, AllowAny

# Serializers
from users.serializers import UserLoginSerializer, UserModelSerializer



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
        #Validate is auth
        permisions = [IsAuthenticated]

        if not request.user:
            return Response({'detail':'No autenticado'},status=status.HTTP_401_UNAUTHORIZED)

        request.user.auth_token.delete()
        res = {
            'msg': 'Cierre de sesion exitoso'
        }
        return Response(res, status=status.HTTP_200_OK)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserModelSerializer(queryset, many=True)
        return Response(serializer.data)