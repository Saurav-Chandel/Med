# from django.contrib import admin
# from django.urls import path, include
# from django.http.response import HttpResponse
# from payments.views import *

# app_name = "payments"

# urlpatterns = [

#     # create subscription 
#     path("api/v1/payment/create/session/", createCheckoutSession.as_view()),
#     path("api/v1/payment/get/session/", getCheckoutSession.as_view()),
#     path("api/v1/payment/verify/",saveSessionDetails.as_view()),
#     path("api/v1/payment/webhook/", paymentStripeWebhook.as_view()),
#     path("api/v1/payment/create-customer-portal-session/", createCustomerPortalSession.as_view()),
#     path("api/v1/payment/list/", paymentList.as_view()),


# ]