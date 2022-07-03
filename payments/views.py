# from django.contrib.auth import models
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework import permissions, status

# from drf_yasg.utils import swagger_auto_schema
# from django.views.decorators.csrf import csrf_exempt
# from user.models import User
# from payments.models import PaymentStripe
# from app.response import *
# # import stripe
# import json
# from drf_yasg import openapi
# from django.shortcuts import redirect
# from django.http import JsonResponse, HttpResponse
# from django.conf import settings
# import math
# from django.db.models import Q
# from payments.serializers import PaymentStripeSerializer
# from rest_framework_simplejwt import authentication


# stripe.api_key = getattr(settings,'STRIPE_API_KEY')


# # Create your views here.
# class createCheckoutSession(APIView):
#     @swagger_auto_schema(
#         operation_description="Create Stripe Checkout Session",
#         operation_summary="Create Stripe Checkout Session",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "user_id": openapi.Schema(
#                     type=openapi.TYPE_INTEGER, description="enter user_id"
#                 )
#             },
#         ),
#     )
#     @csrf_exempt
#     def post(self,request):
#         data = request.data
#         userId = data.get("user_id")
#         try:
#             user = User.objects.get(id=userId)

#             stripe_customer = None
#             if user.stripe_customer_id:
#                 print(":if")
#                 stripe_customer = user.stripe_customer_id
#             else:
#                 stripe_customer = stripe.Customer.create(email=user.email,).id
#                 user.stripe_customer_id = stripe_customer
#                 user.save()

#             # TODO: this is static because only one product need to subscribe
#             prices = stripe.Price.list()
#             checkout_session_details = stripe.checkout.Session.create(
#                 payment_method_types=["card"],
#                 line_items=[
#                     {
#                         'price': str(prices.data[0].id),
#                         'quantity': 1,
#                     },
#                 ],
#                 mode="subscription",
#                 customer=stripe_customer,
#                 payment_behavior='default_incomplete',
#                 expand=['latest_invoice.payment_intent'],
#                 success_url = "https://medical.softuvo.xyz/" + "stripepayment/?token=" + str(userId) + "&status=success",
#                 cancel_url = "https://medical.softuvo.xyz/" + "stripepayment/?token=" + str(userId) + "&status=fail",
#             )

#             payment = PaymentStripe(payment_from=user,checkout_session_details=checkout_session_details,checkout_session_id=checkout_session_details['id'],payment_status='unpaid')
#             payment.save()

#             return ResponseOk({
#                 "checkout_session_id":checkout_session_details['id'],
#                 "checkout_session_url": checkout_session_details.url,
#                 'session':checkout_session_details
#             })

#         except Exception as e:
#             print(e)
#             return ResponseBadRequest({'debug':"session couldn't be created"})


# class getCheckoutSession(APIView):
#     @swagger_auto_schema(
#         operation_description="Get Checkout Session Details",
#         operation_summary="Get Checkout Session Details",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "user_id": openapi.Schema(
#                     type=openapi.TYPE_INTEGER, description="enter user_id"
#                 )
#             },
#         ),
#     )

#     def post(self,request):
#         userId = request.data.get('user_id')
#         try:
#             user = User.objects.get(id=userId)
#             session_id = user.stripe_payment_from.latest('created_at').checkout_session_id
#             checkout_session = stripe.checkout.Session.retrieve(session_id)
#             return ResponseOk({'session':checkout_session})
#         except Exception as e:
#             return ResponseBadRequest({'debug':"session couldn't be created"})

# class saveSessionDetails(APIView):
#     @swagger_auto_schema(
#         operation_description="Get Latest Payment Details",
#         operation_summary="Get Latest Payment Details",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
#                 "status": openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#     )
#     def post(self,request):
#         userId = request.data.get('user_id')
#         status = request.data.get('status')
        
#         try:
#             user = User.objects.get(id=userId)
#             payment_status = user.stripe_payment_from.latest('created_at')
#             payment_status.payment_status = status
#             payment_status.save()
#             return ResponseOk()
#         except Exception as e:
#             return ResponseBadRequest({'debug':"session couldn't be created"})

# class paymentStripeWebhook(APIView):
#     @swagger_auto_schema(
#         operation_description="Stripe Webhook",
#         operation_summary="Stripe Webhook",
#     )
    
#     @csrf_exempt
#     def post(self,request):

#         payload = request.body
#         sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#         event = None

#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#             )
#         except ValueError as e:
#             print(e)
#             # Invalid payload
#             return HttpResponse(status=400)
#         except stripe.error.SignatureVerificationError as e:
#             print(e)
#             # Invalid signature
#             return HttpResponse(status=400)

#         # Handle the checkout.session.completed event
#         # if event['type'] == 'checkout.session.completed':
#         #     session = event['data']['object']

#         #     customer_email = session["customer_details"]["email"]
#         #     product_id = session["metadata"]["product_id"]

#         #     # product = Product.objects.get(id=product_id)

#         #     # send_mail(
#         #     #     subject="Here is your product",
#         #     #     message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
#         #     #     recipient_list=[customer_email],
#         #     #     from_email="matt@test.com"
#         #     # )

#         #     # TODO - decide whether you want to send the file or the URL
        

#         if event['type'] == 'checkout.session.async_payment_failed':
#             session = event['data']['object']
#             user = User.objects.get(stripe_customer_id=session["customer"])
#             user_payment_details = user.stripe_payment_from.latest('created_at')
#             user_payment_details.payment_status = session["payment_status"]
#             user_payment_details.save()

#             print("-------------checkout.session.async_payment_failed-----------------")
#             print(session)
#         elif event['type'] == 'checkout.session.async_payment_succeeded':
#             session = event['data']['object']
#             user = User.objects.get(stripe_customer_id=session["customer"])
#             user_payment_details = user.stripe_payment_from.latest('created_at')
#             user_payment_details.payment_status = session["payment_status"]
#             user_payment_details.save()

#             print("-----------checkout.session.async_payment_succeeded-------------------")
#             print(session)

#         elif event['type'] == 'checkout.session.completed':
#             session = event['data']['object']

#             user = User.objects.get(stripe_customer_id=session["customer"])
#             user_payment_details = user.stripe_payment_from.latest('created_at')
#             user_payment_details.payment_status = session["payment_status"]
#             user_payment_details.save()
#             print("----------checkout.session.completed--------------------")
#             print(session)

#         elif event['type'] == 'checkout.session.expired':
#             session = event['data']['object']
#             user = User.objects.get(stripe_customer_id=session["customer"])
#             user_payment_details = user.stripe_payment_from.latest('created_at')
#             user_payment_details.payment_status = session["payment_status"]
#             user_payment_details.save()

#             print("-----------checkout.session.expired-------------------")
#             print(session)

#         elif event['type'] == 'customer.subscription.created':
#             session = event['data']['object']
#             user = User.objects.get(stripe_customer_id=session["customer"])
#             user.stripe_subscription_status = True
#             user.save()
#             print("-----------customer.subscription.created-------------------")
#             print(session)

#         elif event['type'] == 'customer.subscription.deleted':
#             session = event['data']['object']
#             user = User.objects.get(stripe_customer_id=session["customer"])
#             user.stripe_subscription_status = False
#             user.save()
#             print("-----------customer.subscription.deleted-------------------")
#             print(session)

#         return HttpResponse(status=200)


# class createCustomerPortalSession(APIView):
#     @swagger_auto_schema(
#         operation_description="Get Latest Payment Details",
#         operation_summary="Get Latest Payment Details",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
#             },
#         ),
#     )
#     def post(self,request):
#         userId = request.data.get('user_id')
#         try:
#             user = User.objects.get(id=userId)

#             stripe_customer = None
#             if user.stripe_customer_id:
#                 print(":if")
#                 stripe_customer = user.stripe_customer_id
#             else:
#                 stripe_customer = stripe.Customer.create(email=user.email,).id
#                 user.stripe_customer_id = stripe_customer
#                 user.save()

#             session = stripe.billing_portal.Session.create(customer=stripe_customer, return_url= "https://medical.softuvo.xyz/",)
#             return ResponseOk({
#                 'url':session.url
#             })


#         except Exception as e:
#             print(e)
#             return HttpResponse(status=400)


# class paymentList(APIView):
#     """
#     Get All Transaction List
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [authentication.JWTAuthentication]

#     userId = openapi.Parameter(
#         "UserId",
#         in_=openapi.IN_QUERY,
#         description="userId",
#         type=openapi.TYPE_STRING,
#     )
    
#     page = openapi.Parameter(
#         "page",
#         in_=openapi.IN_QUERY,
#         description="page",
#         type=openapi.TYPE_STRING,
#     )
#     perpage = openapi.Parameter(
#         "perpage",
#         in_=openapi.IN_QUERY,
#         description="perpage",
#         type=openapi.TYPE_STRING,
#     )
#     sort_dir = openapi.Parameter(
#         "sort_dir",
#         in_=openapi.IN_QUERY,
#         description="asc or desc",
#         type=openapi.TYPE_STRING,
#     )
#     sort_field = openapi.Parameter(
#         "sort_field",
#         in_=openapi.IN_QUERY,
#         description="sort_field",
#         type=openapi.TYPE_STRING,
#     )

#     @swagger_auto_schema(
#         manual_parameters=[userId,page,perpage,sort_dir,sort_field]
#     )
#     @csrf_exempt
#     def get(self, request):
#         try:

#             data = request.GET
#             if data.get("UserId"):
#                 UserId = data.get("UserId")
#             else:
#                 UserId = ""   


#             if data.get("page"):
#                 page = data.get("page")
#             else:
#                 page = 1

#             if data.get("perpage"):
#                 limit = data.get("perpage")
#             else:
#                 limit = str(settings.PAGE_SIZE)

#             pages, skip = 1, 0

#             sort_field = data.get("sort_field")

#             sort_dir = data.get("sort_dir")

#             if page and limit:
#                 page = int(page)
#                 limit = int(limit)
#                 skip = (page - 1) * limit
    
#             payment_list = PaymentStripe.objects.all()
#             if UserId:
#                 payment_list = payment_list.filter(
#                     Q(payment_from__id=UserId)
#                 )

#             count = payment_list.count()

#             if sort_field is not None and sort_dir is not None:
#                 if sort_dir == "asc":
#                     if sort_field == "insurance_name":
#                         payment_list = payment_list.order_by("insurance_name")
#                     elif sort_field == "id":
#                         payment_list = payment_list.order_by("id")
#                     else:
#                         payment_list = payment_list.order_by("id")
#                 elif sort_dir == "desc":
#                     if sort_field == "insurance_name":
#                         payment_list = payment_list.order_by("-insurance_name")

#                     elif sort_field == "id":
#                         payment_list = payment_list.order_by("-id")

#                     else:
#                         payment_list = payment_list.order_by("-id")
#             else:
#                 insurance = payment_list.order_by("-id")

#             if page and limit:
#                 insurance = insurance[skip : skip + limit]

#                 pages = math.ceil(count / limit) if limit else 1

#             if insurance:
#                 insurance = PaymentStripeSerializer(insurance, many=True).data

#                 return ResponseOk(
#                     {
#                         "data": insurance,
#                         "meta": {
#                             "page": page,
#                             "total_pages": pages,
#                             "perpage": limit,
#                             "sort_dir": sort_dir,
#                             "sort_field": sort_field,
#                             "total_records": count,
            
#                         },
#                     }
#                 )
#             return ResponseBadRequest("Search query has no match")

#         except Exception as e:
#             return ResponseBadRequest({"debug": str(e)})

