
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token
class UserModelSerializer( serializers.ModelSerializer):
    class Meta:
        model = User
        USERNAME_FIELD = 'username'
        fields = (
            'username',
            'first_name',
            'last_name',
            'is_staff'
        )

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):        
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('Las credenciales no son correctas')

        self.context['user'] = user
        return attrs

    def create(self, validated_data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=20)
    password = serializers.CharField(min_length=8, max_length=64)
    re_password = serializers.CharField(min_length=8, max_length=64)
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)
    is_staff = serializers.BooleanField(default=False)
    
    
    def validate(self, attrs):
        password = attrs['password']
        re_password = attrs['re_password']
        password_validation.validate_password(password)

        if password != re_password:
            raise serializers.ValidationError('Las contraseñas no coinciden')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            password=validated_data['password'],
            is_staff=validated_data['is_staff'])
        return user

class UserEditSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.save()
        return instance

class UserChangesPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)
    re_password = serializers.CharField(min_length=8, max_length=64)

    def validate(self,data):
        password = data['password']
        re_password = data['re_password']
        password_validation.validate_password(password)

        if password != re_password:
            raise serializers.ValidationError('Las contraseñas no coinciden')
        return data

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError('La contraseña actual no es correcta')

        instance.set_password(validated_data['password'])
        instance.save()
        return instance