# amankan/api/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q
from rest_framework import exceptions, status
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    def validate(self, attrs):
        # Ambil email atau username dan password dari request
        email_or_username = attrs.get(self.username_field)
        password = attrs.get('password')
        
        # Cek apakah user ada (berdasarkan email atau username)
        try:
            user = User.objects.get(
                Q(username=email_or_username) | Q(email=email_or_username)
            )
            
            # Verifikasi password
            if not user.check_password(password):
                raise exceptions.AuthenticationFailed(
                    'Wrong Password. Please Try Again',
                    code='invalid_password'
                )
                
            # Jika user tidak aktif
            if not user.is_active:
                raise exceptions.AuthenticationFailed(
                    'Your account has been deactivated. Please contact the administrator.',
                    code='user_inactive'
                )
                
            # Generate token
            refresh = self.get_token(user)
            
            # Update last login
            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, user)
                
            # Buat response data
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
            
            return data
            
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'An account with this email/username was not found.',
                code='user_not_found'
            )