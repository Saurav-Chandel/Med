from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Token ,Media
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, serializers, status, viewsets
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from app.response import *
from app.util import *
from user import serializers as user_serializers
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import (
    DjangoUnicodeDecodeError,
    smart_bytes,
    smart_str,
)
from django.http import Http404, HttpResponsePermanentRedirect

from django.contrib.sites.shortcuts import get_current_site

from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

# from rest_framework_jwt.settings import api_settings
from django.contrib.auth import login, authenticate
from main import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse 
from app.SendinSES import *
from rest_framework.parsers import FormParser, MultiPartParser
# Create your views here.


class LoginView(APIView):
    """
    login user api
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        operation_description="User login API",
        operation_summary="User login API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    @csrf_exempt
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        try:
            user_object = User.objects.get(email=email)
        except User.DoesNotExist:
            return ResponseBadRequest(
                {
                    "data": "User not found",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Serializer error",
                }
            )

        if user_object.check_password(password):
            print("password match")
            token = RefreshToken.for_user(user_object)
            print(token)
            if not Token.objects.filter(
                token_type="access_token", user_id=user_object.id
            ).exists():
                Token.objects.create(
                    user_id=user_object.id,
                    token=str(token.access_token),
                    token_type="access_token",
                )
            else:
                Token.objects.filter(
                    user_id=user_object.id, token_type="access_token"
                ).update(token=str(token.access_token))
            serializer = user_serializers.UserSerializer(user_object)

            return Response(
                {
                    "data": serializer.data,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
                    "code": status.HTTP_200_OK,
                    "message": "Login SuccessFully",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return ResponseBadRequest(
                {
                    "data": "wrong credentials",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Serializer error",
                }
            )


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        operation_description="User Sign up API",
        operation_summary="User Sign up API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "first_last_name": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "phone_no": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    @csrf_exempt
    def post(self, request):
        data = request.data
        data["username"] = data['email']


        if User.objects.filter(username=data["username"]).exists():
            return ResponseBadRequest(
                {
                    "data": {"email": ["Email Already Exist"]},
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Serializer error",
                }
            )

        serializer = user_serializers.UserSignupSerializer(data=data)

        # if not validate_phone_number(data.get("phone_no")):
        #     return ResponseBadRequest(
        #         {
        #             "data": {"phone_no": ["Invalid Phone Number"]},
        #             "code": status.HTTP_400_BAD_REQUEST,
        #             "message": "Serializer error",
        #         }
        #     )

        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "User created successfully",
                }
            )
        else:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Serializer error",
                }
            )

class LogoutView(APIView):
    """
    Logout user api
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Log the authenticated user out",
        operation_summary="Log the authenticated user out",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    @csrf_exempt
    def post(self, request):

        serializer = user_serializers.LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Password reset email",
        operation_summary="Password reset email",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "redirect_url": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="enter redirect url example: https://www.google.com",
                ),
            },
        ),
    )
    @csrf_exempt
    def post(self, request):

        data = request.data
        email = data.get("email")
        redirect_url = data.get("redirect_url")

        if User.objects.filter(
            email=email
        ).exists():
            user = User.objects.get(
                email=email
            )

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                "user:forgot-password-confirm",
                kwargs={"uidb64": uidb64, "token": token},
            )

            absurl = (
                "http://"
                + current_site
                + relativeLink
                +"?redirect_url="
                + redirect_url
                
            )
            email_body = (
                "Hello, \n Use link below to reset your password  \n" + absurl
            )
            print("_________________")
        
            send_reset_password_mail(request, user.email, email_body)
            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )
        else:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "User Does Not Exist",
                }
            )

class PasswordTokenCheckAPIView(APIView):
    serializer_class = user_serializers.SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    def get(self, request, uidb64, token):

        redirect_url = request.GET.get("redirect_url")

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return HttpResponsePermanentRedirect(
                    redirect_url + "?token_valid=False"
                )
  
            if redirect_url and len(redirect_url) > 3:
                return HttpResponsePermanentRedirect(
                    redirect_url
                    + "?token_valid=True&uidb64="
                    + uidb64
                    + "&token="
                    + token
                )
            else:
                return HttpResponsePermanentRedirect(
                    redirect_url + "?token_valid=False"
                )

        except DjangoUnicodeDecodeError as identifier:

            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return HttpResponsePermanentRedirect(
                        redirect_url + "?token_valid=False"
                    )

            except UnboundLocalError as e:
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

class SetNewPasswordAPIView(APIView):
    serializer_class = user_serializers.SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        operation_description="Set new password",
        operation_summary="Set new password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "token": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="token",
                ),
                "uidb64": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="uidb64",
                ),
            },
        ),
    )
    @csrf_exempt
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @swagger_auto_schema(
        operation_description="User reset password API",
        operation_summary="User reset password API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "current_password": openapi.Schema(type=openapi.TYPE_STRING),
                "new_password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    @csrf_exempt
    def post(self, request):
        """
        User Password Reset - From the Profile Settings.
        :param request:
        :param format:
        :return:
        """
        data = request.data
        user = request.user
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not validate_password(current_password) and not validate_password(
            new_password
        ):
            return ResponseBadRequest(
                (
                    {
                        "result": "error",
                        "errorText": "Invalid Current Password and New Password",
                    }
                )
            )
        if not validate_password(current_password):
            return ResponseBadRequest(
                (
                    {
                        "result": "error",
                        "errorText": "New Password matches the old one"
                    }
                )
            )
        if not validate_password(new_password):
            return ResponseBadRequest(
                (
                    {
                        "result": "error",
                        "errorText": "New Password matches the old one"
                    }
                )
            )
        if (
            current_password == new_password
            or new_password_matches_old_password(new_password, user.password)
        ):
            return ResponseBadRequest(
                (
                    {
                        "result": "error",
                        "errorText": "New Password matches the old one"
                    }
                )
            )
        if not new_password_matches_old_password(
            current_password, user.password
        ):
            return ResponseBadRequest(
                (
                    {
                        "result": "error",
                        "errorText": "Incorrect Credentials"
                    }
                )
            )
        try:
            user.set_password(new_password)
            user.save()
            return ResponseOk()
        except Exception as e:
            return ResponseInternalServerError(str(e))


class UpdateProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="User reset password API",
        operation_summary="User reset password API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "first_last_name": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "phone_no": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    @csrf_exempt
    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = user_serializers.UpdateProfileProfileSerializer(
            profile, data=request.data
        )
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetAllMedia(APIView):
    """
    Get All Media
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get(self, request):

        try:
            media = Media.objects.all()

            serializer = user_serializers.MediaSerializer(media, many=True)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "Media list",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Media Does Not Exist",
                }
            )


class CreateMedia(APIView):
    """
    Create Media
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)
    @swagger_auto_schema(
        operation_description="Upload file...",
        request_body=user_serializers.CreateMediaSerializer,
    )
    @csrf_exempt
    def post(self, request):
        serializer = user_serializers.CreateMediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "Media created succesfully",
                }
            )
        else:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Media is not valid",
                }
            )


class GetMedia(APIView):
    """
    Get Media by pk
    """
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            raise ResponseNotFound()

    @csrf_exempt
    def get(self, request, pk):
        try:
            media = self.get_object(pk)
            serializer = user_serializers.MediaSerializer(media)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get Media successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Media Does Not Exist",
                }
            )



class UpdateMedia(APIView):
    """
    Update Media
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self, pk):
        try:
            return Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            raise ResponseNotFound()
    @swagger_auto_schema(
        operation_description="Upload file...",
        request_body=user_serializers.CreateMediaSerializer,
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            media = self.get_object(pk)
            serializer = user_serializers.CreateMediaSerializer(media, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "Media updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Media Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Media Does Not Exist",
                }
            )



class DeleteMedia(APIView):
    """
    Delete Media
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            raise ResponseNotFound()

    @csrf_exempt
    def delete(self, request, pk):
        try:
            media = self.get_object(pk)
            media.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Media deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Media Does Not Exist",
                }
            )












































































