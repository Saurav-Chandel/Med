"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wqqc93e*z@1&o#gv&frb=4fbp3bv6^pu4-!i2*&g1l*uj)(i*-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django_extensions',
    'user',
    'hospital',
    'insurance',
    'review',
    'payments',
    "app",
    'rest_framework',
    'drf_yasg',
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist", 
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("RDS_DB_NAMeeEEE", "akshit-mountain"),
        "USER": os.environ.get("RDS_USERNAeeME", "postgres"),
        "PASSWORD": os.environ.get("ee", "root"),
        "HOST": os.environ.get("RDS_HeeeOSTNAME", "127.0.0.1"),
        "PORT": os.environ.get("eeeeeeeee", "5432"),
        "TIME_ZONE": "Asia/Kolkata",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # Parser classes priority-wise for Swagger
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.JSONParser",
    ],
    # "EXCEPTION_HANDLER": "app.util.permission_error_handler",
}


SWAGGER_SETTINGS = {
    "DOC_EXPANSION": "none",
    "TAGS_SORTER": "alpha",
    "OPERATIONS_SORTER": "alpha",
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": datetime.timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": datetime.timedelta(days=1),
}



AUTH_USER_MODEL='user.User'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
MEDIA_ROOT = os.path.join(BASE_DIR, "media_root")
STATIC_URL = "/static_url/"
MEDIA_URL = "/media_url/"
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = [
"https://medical.softuvo.xyz",
"http://medical.softuvo.xyz",
"https://medicalapi.softuvo.xyz",
"http://medicalapi.softuvo.xyz",
"http://localhost:3080",
"http://127.0.0.1:3000",
"http://127.0.0.1:8000",
"http://192.168.1.221:8000",
]


CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CSRF_TRUSTED_ORIGINS = [
    "https://medical.softuvo.xyz",
    "http://medical.softuvo.xyz",
    "https://medicalapi.softuvo.xyz",
    "http://medicalapi.softuvo.xyz",
]


# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USERR", "rajesh.kumar75395187@gmail.com") #config("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORDD", "Softuvo@1234")  #config("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PAGE_SIZE=20
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "email-smtp.ap-south-1.amazonaws.com"
EMAIL_HOST_USER ="AKIAQS6B3M3MLWU55N2K" #config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD ="BB1KWtSAP4050xdDvojsEvZ7jQGS29GybjBcPPdo6x7i"  #config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER