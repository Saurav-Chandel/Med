import re

import phonenumbers
import pyotp
from django.contrib.auth.hashers import make_password
from rest_framework.views import exception_handler

from user.models import User

MIN_PASSWORD_LENGTH = 5


def validate_email(email):
    """
    Function to validate email address
    :param email:
    :return:
    """
    if not email:
        return False
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(regex, email):
        return True
    return False


def validate_password(password):
    """
    Function to validate a password
    :param password:
    :return:
    """
    if not password or len(password) < MIN_PASSWORD_LENGTH:
        return False
    return True


def validate_phone_number(phone):
    """
    from TeamEstatesRealty.utils.util_functions import validate_phone_number as vpn
    """
    if not phone:
        return False
    if str(phone).startswith("+"):
        ph = phonenumbers.parse(phone)
        return phonenumbers.is_valid_number(ph)
    if len(phone) > 12:
        return False
    regex = r"[123456789]\d{9}$"
    if re.search(regex, phone):
        return True
    return False


def permission_error_handler(exc, context):
    """
    Function to modify the results when the permissions are not sent
    """
    response = exception_handler(exc, context)
    print("response ", response)
    if response.status_code == 403:
        response.data = {
            "success": 0,
            "error": response.data["detail"],
            "status": 403,
        }
    if response.status_code == 401:
        response.data = {
            "success": 0,
            "error": response.data["detail"],
            "status": 401,
        }
    return response


def new_password_matches_old_password(password, password_hash):
    """
    Function to check if the new password matches the currently set password.
    :param password: new raw password
    :param password_hash: current password hash.
    :return: True if new password matches the old one.
    """
    if not password_hash:
        return False
    salt = password_hash.split("$")[-2]
    new_hash = make_password(password, salt)
    return new_hash == password_hash


def is_string_a_number(string):
    """
    Function to check if a String is a number or not
    """
    if None:
        return None
    try:
        return float(string)
    except:
        return False


def get_user_object(company_domain, email):
    """
    Function to get user object from user table
    """
    try:
        return User.objects.get(
            email=email, user_company__url_domain=company_domain
        )
    except:
        return None


def generate_otp():
    """
    Function to get otp
    """
    otp = pyotp.random_base32()
    time_otp = pyotp.TOTP(otp, interval=300)

    # TODO: update otp length based on UI
    return time_otp.now()[:5]
