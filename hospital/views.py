from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from .models import *
from .serializers import *
from rest_framework import permissions, status
from rest_framework_simplejwt import authentication
from app.response import ResponseBadRequest, ResponseNotFound, ResponseOk
from django.conf import settings
from django.db.models import Q
import math
from rest_framework.parsers import FormParser, MultiPartParser

# Create your views here.

class GetAllHospital(APIView):
    """
    Get All Hospital
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    search = openapi.Parameter(
        "search",
        in_=openapi.IN_QUERY,
        description="search",
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
    zip_code = openapi.Parameter(
        "zip_code",
        in_=openapi.IN_QUERY,
        description="search hospital by zip_code",
        type=openapi.TYPE_STRING,
    )
    distance = openapi.Parameter(
        "distance",
        in_=openapi.IN_QUERY,
        description="search hospital by distance",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        manual_parameters=[
            search,
            page,
            perpage,
            sort_dir,
            sort_field,
            zip_code,
            distance
        ]
    )
    @csrf_exempt
    def get(self, request):
        try:
            data = request.GET

            if data.get("search"):
                query = data.get("search")
            else:
                query = ""

            if data.get("zip_code"):
                zip = data.get("zip_code")
            else:
                zip = ""    

            if data.get("distance"):
                distance = data.get("distance")
            else:
                distance = ""        

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

            hospital = Hospital.objects.all()

            if query:
                hospital = hospital.filter(
                    Q(hospital_name__icontains=query) | Q(zip_code__icontains=query)
                )
            if zip:
                hospital=hospital.filter(zip_code=zip)    

            if distance:
                hospital=hospital.filter(distance=distance)   

            count = hospital.count()

            if sort_field is not None and sort_dir is not None:
                if sort_dir == "asc":
                    if sort_field == "hospital_name":
                        hospital = hospital.order_by("hospital_name")
                    elif sort_field == "specialization":
                        hospital = hospital.order_by("specialization")
                    elif sort_field == "id":
                        hospital = hospital.order_by("id")
                    else:
                        hospital = hospital.order_by("id")
                elif sort_dir == "desc":
                    if sort_field == "hospital_name":
                        hospital = hospital.order_by("-hospital_name")
                    elif sort_field == "specialization":
                        hospital = hospital.order_by("-specialization")
                    elif sort_field == "id":
                        hospital = hospital.order_by("-id")

                    else:
                        hospital = hospital.order_by("-id")
            else:
                hospital = hospital.order_by("-id")

            if page and limit:
                hospital = hospital[skip : skip + limit]

                pages = math.ceil(count / limit) if limit else 1
            if hospital:
                hospital = HospitalSerializer(hospital, many=True).data

                return ResponseOk(
                    {
                        "data": hospital,
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
            return ResponseBadRequest("Search query has no match")

        except Exception as e:
            return ResponseBadRequest({"debug": str(e)})



class CreateHospital(APIView):
    """
    Create Hospital
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_description="Hospital create API",
        operation_summary="Hospital create API",
        request_body=CreateHospitalSerializer,
        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     properties={
        #         "hospital_name": openapi.Schema(type=openapi.TYPE_STRING),
        #         "latitude": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "longitude": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "specialization": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "info": openapi.Schema(type=openapi.TYPE_STRING),
        #         "address": openapi.Schema(type=openapi.TYPE_STRING),
        #         "zip_code": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "phone_no": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "distance": openapi.Schema(type=openapi.TYPE_INTEGER),
        #     },
        # ),
    )
    @csrf_exempt
    def post(self, request):
        serializer = CreateHospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "Hospital created succesfully",
                }
            )
        else:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Hospital is not valid",
                }
            )



class GetHospital(APIView):
    """
    Get Hospital by pk
    """
    
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    csrf_exempt

    def get_object(self, pk):
        try:
            return Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            hospital = self.get_object(pk)
            serializer = HospitalSerializer(hospital)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get Hospital successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Hospital Does Not Exist",
                }
            )

class UpdateHospital(APIView):
    """
    Update Hospital
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self, pk):
        try:
            return Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="Hospital update API",
        operation_summary="Hospital update API",
        request_body=CreateHospitalSerializer,

        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     properties={
        #         "hospital_name": openapi.Schema(type=openapi.TYPE_STRING),
        #         "latitude": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "longitude": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "specialization": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "info": openapi.Schema(type=openapi.TYPE_STRING),
        #         "address": openapi.Schema(type=openapi.TYPE_STRING),
        #         "zip_code": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "phone_no": openapi.Schema(type=openapi.TYPE_INTEGER),
        #         "distance": openapi.Schema(type=openapi.TYPE_INTEGER),
        #     },
        # ),
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            hospital = self.get_object(pk)
            serializer = CreateHospitalSerializer(hospital, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "Hospital updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Hospital Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Hospital Does Not Exist",
                }
            )



class DeleteHospital(APIView):
    """
    Delete Hospital
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get_object(self, pk):
        try:
            return Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            hospital = self.get_object(pk)
            hospital.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Hospital deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Hospital Does Not Exist",
                }
            )



class GetAllSpecialization(APIView):
    """
    Get All Specialization
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    search = openapi.Parameter(
        "search",
        in_=openapi.IN_QUERY,
        description="search",
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
    zip_code = openapi.Parameter(
        "zip_code",
        in_=openapi.IN_QUERY,
        description="search specialization on the basis of zip_code",
        type=openapi.TYPE_STRING,
    )
 
    @swagger_auto_schema(
        manual_parameters=[
            search,
            page,
            perpage,
            sort_dir,
            sort_field,
            zip_code
        ]
    )
    @csrf_exempt
    def get(self, request):
        try:
            data = request.GET

            if data.get("search"):
                query = data.get("search")
            else:
                query = ""

            if data.get("zip_code"):
                zip = data.get("zip_code")
            else:
                zip = ""   
            print(zip)     

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

            specialization = Specialization.objects.all()

            if query:
                specialization = specialization.filter(
                    Q(name__icontains=query)
                )
            if zip:
                specialization=specialization.filter(hospital_specialization__zip_code=zip)
                print(specialization)
                
            count = specialization.count()

            if sort_field is not None and sort_dir is not None:
                if sort_dir == "asc":
                    if sort_field == "name":
                        specialization = specialization.order_by("name")
                 
                    elif sort_field == "id":
                        specialization = specialization.order_by("id")
                    else:
                        specialization = specialization.order_by("id")
                elif sort_dir == "desc":
                    if sort_field == "name":
                        specialization = specialization.order_by("-name")
                 
                    elif sort_field == "id":
                        specialization = specialization.order_by("-id")

                    else:
                        specialization = specialization.order_by("-id")
            else:
                specialization = specialization.order_by("-id")

            if page and limit:
                specialization = specialization[skip : skip + limit]

                pages = math.ceil(count / limit) if limit else 1
            if specialization:
                specialization = SpecializationSerializer(specialization, many=True).data

                return ResponseOk(
                    {
                        "data": specialization,
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
            return ResponseBadRequest("Search query has no match")

        except Exception as e:
            return ResponseBadRequest({"debug": str(e)})



class CreateSpecialization(APIView):
    """
    Create Specialization
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Specialization create API",
        operation_summary="Specialization create API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    @csrf_exempt
    def post(self, request):
        serializer = SpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "Specialization created succesfully",
                }
            )
        else:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Specialization is not valid",
                }
            )



class GetSpecialization(APIView):
    """
    Get Specialization by pk
    """
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    csrf_exempt

    def get_object(self, pk):
        try:
            return Specialization.objects.get(pk=pk)
        except Specialization.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            specialization = self.get_object(pk)
            serializer = SpecializationSerializer(specialization)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get Specialization successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Specialization Does Not Exist",
                }
            )




class UpdateSpecialization(APIView):
    """
    Update Specialization
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Specialization.objects.get(pk=pk)
        except Specialization.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="Specialization update API",
        operation_summary="Specialization update API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
              
            },
        ),
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            specialization = self.get_object(pk)
            serializer = SpecializationSerializer(specialization, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "Specialization updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Specialization Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Specialization Does Not Exist",
                }
            )



class DeleteSpecialization(APIView):
    """
    Delete Specialization
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get_object(self, pk):
        try:
            return Specialization.objects.get(pk=pk)
        except Specialization.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            specialization = self.get_object(pk)
            specialization.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Specialization deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Specialization Does Not Exist",
                }
            )


