import math
from django.shortcuts import render
from django.conf import settings
from django.db.models import F, Q
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from app.response import ResponseBadRequest, ResponseNotFound, ResponseOk
from .models import *
from .serializers import *
from rest_framework.parsers import FormParser, MultiPartParser

# Create your views here.


class GetAllReview(APIView):
    """
    Get All Review
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    search = openapi.Parameter(
        "search",
        in_=openapi.IN_QUERY,
        description="search Review",
        type=openapi.TYPE_STRING,
    )
    hospital = openapi.Parameter(
        "hospital",
        in_=openapi.IN_QUERY,
        description="search reviews by hospital_id",
        type=openapi.TYPE_STRING,
    )
    page = openapi.Parameter(
        "page",
        in_=openapi.IN_QUERY,
        description="page",
        type=openapi.TYPE_STRING,
    )
    perpage = openapi.Parameter(
        "perpage",
        in_=openapi.IN_QUERY,
        description="perpage",
        type=openapi.TYPE_STRING,
    )
    sort_dir = openapi.Parameter(
        "sort_dir",
        in_=openapi.IN_QUERY,
        description="asc or desc",
        type=openapi.TYPE_STRING,
    )
    sort_field = openapi.Parameter(
        "sort_field",
        in_=openapi.IN_QUERY,
        description="sort_field",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        manual_parameters=[search, page, perpage, sort_dir, sort_field,hospital]
    )
    @csrf_exempt
    def get(self, request):
        try:
            data = request.GET
            if data.get("search"):
                query = data.get("search")
            else:
                query = ""

            if data.get("hospital"):
                hospital_id = data.get("hospital")
            else:
                hospital_id = ""    

            if data.get("page"):
                page = data.get("page")
            else:
                page = 1

            if data.get("perpage"):
                limit = data.get("perpage")
            else:
                limit = str(settings.PAGE_SIZE)

            pages, skip = 1, 0

            sort_field = data.get("sort_field")

            sort_dir = data.get("sort_dir")

            if page and limit:
                page = int(page)
                limit = int(limit)
                skip = (page - 1) * limit

            review = Review.objects.all()

            if query:
                review = review.filter(
                   
                      Q(rating__icontains=query)
                    | Q(review__icontains=query)
                )
            if hospital_id:
                review=review.filter(hospital=hospital_id)    

            count = review.count()

            if sort_field is not None and sort_dir is not None:
                if sort_dir == "asc":
                    if sort_field == "review":
                        review = review.order_by("review")
                    elif sort_field == "hospital":
                        review = review.order_by("hospital")
                    elif sort_field == "procedure":
                        review = review.order_by("-procedure")    
                    elif sort_field == "id":
                        review = review.order_by("id")

                    else:
                        review = review.order_by("id")
                elif sort_dir == "desc":
                    if sort_field == "review":
                        review = review.order_by("-review")
                    elif sort_field == "hospital":
                        review = review.order_by("-hospital")
                    elif sort_field == "procedure":
                        review = review.order_by("-procedure")    
                    elif sort_field == "id":
                        review = review.order_by("-id")

                    else:
                        review = review.order_by("-id")
            else:
                review = review.order_by("-id")

            if page and limit:
                review = review[skip : skip + limit]

                pages = math.ceil(count / limit) if limit else 1
            if count == 0:
                review = "Review is not available as per hospital id"

            else:
                review = ReviewSerializer(review, many=True).data


            return ResponseOk(
                {
                    "data": review,
                    "meta": {
                        "page": page,
                        "total_pages": pages,
                        "perpage": limit,
                        "sort_dir": sort_dir,
                        "sort_field": sort_field,
                        "total_records": count,
                    },
                }
            )

        except Exception as e:
            return ResponseBadRequest({"debug": str(e)})



class CreateReview(APIView):
    """
    Create Review
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)
    
    @swagger_auto_schema(
        operation_description="Upload file...",
        request_body=ReviewSerializer,
    )
    @csrf_exempt
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "Review created succesfully",
                }
            )
        else:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Review is not valid",
                }
            )


class GetReview(APIView):
    """
    Get Review by pk
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    csrf_exempt

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            review = self.get_object(pk)
            serializer = ReviewSerializer(review)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get Review successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Review Does Not Exist",
                }
            )


class UpdateReview(APIView):
    """
    Update Review
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise ResponseNotFound()

    
    @swagger_auto_schema(
        operation_description="Upload file...",
        request_body=ReviewSerializer,
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            review = self.get_object(pk)
            serializer = CreateReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "Review updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Review Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Review Does Not Exist",
                }
            )


class DeleteReview(APIView):
    """
    Delete Review
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            review = self.get_object(pk)
            review.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Review deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Review Does Not Exist",
                }
            )
