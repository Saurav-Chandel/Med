from rest_framework import serializers
from .models import User ,Media
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.encoding import (
    DjangoUnicodeDecodeError,
    force_str,
    smart_bytes,
    smart_str,
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("id", "username","first_last_name","phone_no","password","email")
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_last_name=validated_data['first_last_name'],
            phone_no=validated_data['phone_no'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = "__all__"
        # fields=("email","password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True
    )
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
  
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:

            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            raise serializers.ValidationError("invalid token")        


class UpdateProfileProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","first_last_name","email","phone_no")

    def update(self, instance, validated_data):
        instance.first_last_name = validated_data.get('first_last_name', instance.first_last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.username=instance.email
        instance.save()

        return instance


class MediaSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Media
        fields = "__all__"


class CreateMediaSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Media
        fields = "__all__"
