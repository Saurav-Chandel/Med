from json import dumps

import requests
from django.core.mail import send_mail
from rest_framework import status

from app.response import ResponseBadRequest
from main import settings


def send_email_otp(request, user_email, email_otp):
    """
    Send Email OTP
    """

    if user_email and email_otp:
        message = (
            "Your One Time Passcode is {} to activate your account.".format(
                email_otp
            )
        )
        from_email = settings.EMAIL_HOST_USER
        to_email = user_email
        try:
            return send_mail(
                "Email Verification<Don't Reply>",
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Something wrong contact admin",
                }
            )
    else:
        return ResponseBadRequest(
            {
                "data": None,
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Something wrong contact admin",
            }
        )


def email_verification_success(request, user_email):
    """
    Email OTP verification success
    """

    if user_email:
        message = "Your Account is activated"
        from_email = settings.EMAIL_HOST_USER
        to_email = user_email
        try:
            return send_mail(
                "Account activated<Don't Reply>",
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Something wrong contact admin",
                }
            )
    else:
        return ResponseBadRequest(
            {
                "data": None,
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Something wrong contact admin",
            }
        )


def send_reset_password_mail(request, user_email, email_body):
    """
    Send Reset Password Mail
    """
    print("++++++++++++==")

    if user_email and email_body:
        Message = email_body
        from_email = settings.EMAIL_HOST_USER
        to_email = user_email
        try:
            send_mail(
                "Reset your passsword<Don't Reply>",
                Message,
                from_email,
                [to_email],
                fail_silently=False,
            )
        except Exception as e:
            return e
    return None
