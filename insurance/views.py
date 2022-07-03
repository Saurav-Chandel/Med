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
import math
from django.conf import settings
from django.db.models import Q

# Create your views here.



class GetAllInsurance(APIView):
    """
    Get All Insurance
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    search = openapi.Parameter(
        "search",
        in_=openapi.IN_QUERY,
        description="search Insurance",
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
        manual_parameters=[search,page,perpage,sort_dir,sort_field]
    )
    @csrf_exempt
    def get(self, request):
        try:

            data = request.GET
            if data.get("search"):
                query = data.get("search")
            else:
                query = ""   


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
    
            insurance = Insurance.objects.all()
            if query:
              
                insurance = insurance.filter(
                    Q(insurance_name__icontains=query)
                )

            count = insurance.count()

            if sort_field is not None and sort_dir is not None:
                if sort_dir == "asc":
                    if sort_field == "insurance_name":
                        insurance = insurance.order_by("insurance_name")
                    elif sort_field == "id":
                        insurance = insurance.order_by("id")
                    else:
                        insurance = insurance.order_by("id")
                elif sort_dir == "desc":
                    if sort_field == "insurance_name":
                        insurance = insurance.order_by("-insurance_name")
                  
                    elif sort_field == "id":
                        insurance = insurance.order_by("-id")

                    else:
                        insurance = insurance.order_by("-id")
            else:
                insurance = insurance.order_by("-id")

            if page and limit:
                insurance = insurance[skip : skip + limit]

                pages = math.ceil(count / limit) if limit else 1
              

            if insurance:
                insurance = InsuranceSerializer(insurance, many=True).data

                return ResponseOk(
                    {
                        "data": insurance,
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



class CreateInsurance(APIView):
    """
    Create Insurance
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Insurance create API",
        operation_summary="Insurance create API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "insurance_name": openapi.Schema(type=openapi.TYPE_STRING),
             
            
            },
        ),
    )
    @csrf_exempt
    def post(self, request):
        serializer = CreateInsuranceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK, 
                    "message": "Insurance created succesfully",
                }
            )
        else:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Insurance is not valid",
                }
            )



class GetInsurance(APIView):
    """
    Get Insurance by pk
    """
    
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.JWTAuthentication]

    csrf_exempt

    def get_object(self, pk):
        try:
            return Insurance.objects.get(pk=pk)
        except Insurance.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            insurance = self.get_object(pk)
            serializer = InsuranceSerializer(insurance)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get Insurance successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Insurance Does Not Exist",
                }
            )




class UpdateInsurance(APIView):
    """
    Update Insurance
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Insurance.objects.get(pk=pk)
        except Insurance.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="Insurance update API",
        operation_summary="Insurance update API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "insurance_name": openapi.Schema(type=openapi.TYPE_STRING),
          
            },
        ),
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            insurance = self.get_object(pk)
            serializer = CreateInsuranceSerializer(insurance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "Insurance updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Insurance Not valid",
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



class DeleteInsurance(APIView):
    """
    Delete Insurance
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get_object(self, pk):
        try:
            return Insurance.objects.get(pk=pk)
        except Insurance.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            insurance = self.get_object(pk)
            insurance.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Insurance deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Insurance Does Not Exist",
                }
            )


class GetAllProcedure(APIView):
    """
    Get All Procedure
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    search = openapi.Parameter(
        "search",
        in_=openapi.IN_QUERY,
        description="search procedure",
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
        manual_parameters=[search,page,perpage,sort_dir,sort_field]
    )
    @csrf_exempt
    def get(self, request):
        try:

            data = request.GET
            if data.get("search"):
                query = data.get("search")
            else:
                query = ""   

           
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

            procedure = Procedure.objects.all()
            
            if query:
                
                procedure = procedure.filter(
                    Q(procedure_name__icontains=query)
                )

            count = procedure.count()

            if sort_field is not None and sort_dir is not None:
                if sort_dir == "asc":
                    if sort_field == "procedure_name":
                        procedure = procedure.order_by("procedure_name")
                   
                    elif sort_field == "id":
                        procedure = procedure.order_by("id")
                    else:
                        procedure = procedure.order_by("id")
                elif sort_dir == "desc":
                    if sort_field == "procedure_name":
                        procedure = procedure.order_by("-procedure_name")
                 
                    elif sort_field == "id":
                        procedure = procedure.order_by("-id")

                    else:
                        procedure = procedure.order_by("-id")
            else:
                procedure = procedure.order_by("-id")

            if page and limit:
                procedure = procedure[skip : skip + limit]

                pages = math.ceil(count / limit) if limit else 1

            if procedure:
                procedure = ProcedureSerializer(procedure, many=True).data

                return ResponseOk(
                    {
                        "data": procedure,
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



class CreateProcedure(APIView):
    """
    Create Procedure
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Procedure create API",
        operation_summary="Procedure create API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "procedure_name": openapi.Schema(type=openapi.TYPE_STRING),
                "billing_code": openapi.Schema(type=openapi.TYPE_INTEGER),
                "revenue_code": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    @csrf_exempt
    def post(self, request):
        serializer = ProcedureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "Procedure created succesfully",
                }
            )
        else:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Procedure is not valid",
                }
            )



class GetProcedure(APIView):
    """
    Get Procedure by pk
    """
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    csrf_exempt

    def get_object(self, pk):
        try:
            return Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            procedure = self.get_object(pk)
            serializer = ProcedureSerializer(procedure)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get Procedure successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Procedure Does Not Exist",
                }
            )




class UpdateProcedure(APIView):
    """
    Update Procedure
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="Procedure update API",
        operation_summary="Procedure update API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "procedure_name": openapi.Schema(type=openapi.TYPE_STRING),
                "billing_code": openapi.Schema(type=openapi.TYPE_INTEGER),
                "revenue_code": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            procedure = self.get_object(pk)
            serializer = ProcedureSerializer(procedure, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "Procedure updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Procedure Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Procedure Does Not Exist",
                }
            )



class DeleteProcedure(APIView):
    """
    Delete Procedure
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get_object(self, pk):
        try:
            return Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            procedure = self.get_object(pk)
            procedure.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Procedure deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Procedure Does Not Exist",
                }
            )



class GetAllCharge(APIView):
    """
    Get All Charges
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = []


    insurance = openapi.Parameter(
        "insurance",
        in_=openapi.IN_QUERY,
        description="search insurance by insuracne_name",
        type=openapi.TYPE_STRING,
    )

    hospital = openapi.Parameter(
        "hospital",
        in_=openapi.IN_QUERY,
        description="search hospital by hospital_name",
        type=openapi.TYPE_STRING,
    )

    zip_code = openapi.Parameter(
        "zip_code",
        in_=openapi.IN_QUERY,
        description="search zip_code",
        type=openapi.TYPE_STRING,
    )

    procedure = openapi.Parameter(
        "procedure",
        in_=openapi.IN_QUERY,
        description="search procedures by procedure_name",
        type=openapi.TYPE_STRING,
    )

    specialization = openapi.Parameter(
        "specialization",
        in_=openapi.IN_QUERY,
        description="search specialization",
        type=openapi.TYPE_STRING,
    )

    hospital_array_id = openapi.Parameter(
        "hospital_array_id",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_INTEGER),
        description="search hospital_array_id",
    )
    specialization_array_id = openapi.Parameter(
        "specialization_array_id",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_INTEGER),
        description="search specialization_array_id",
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
    price1 = openapi.Parameter(
        "price1",
        in_=openapi.IN_QUERY,
        description="less than 100",
        type=openapi.TYPE_STRING,
    )
    price2 = openapi.Parameter(
        "price2",
        in_=openapi.IN_QUERY,
        description="100,500",
        type=openapi.TYPE_STRING,
    )
    price3 = openapi.Parameter(
        "price3",
        in_=openapi.IN_QUERY,
        description="greater than 500",
        type=openapi.TYPE_STRING,
    )
    
    @swagger_auto_schema(
        manual_parameters=[insurance,hospital,procedure,hospital_array_id,specialization_array_id, zip_code,specialization, page,perpage,sort_dir,sort_field,price1,price2,price3]
    )
    @csrf_exempt
    def get(self, request):
        try:
            data=request.GET
            if data.get("insurance"):
                insurance = data.get("insurance")
            else:
                insurance = ""  

            if data.get("zip_code"):
                zip_code = data.get("zip_code")
            else:
                zip_code = ""

            if data.get("hospital"):
                hospital = data.get("hospital")
            else:
                hospital = ""
    
            if data.get("procedure"):
                procedure_name = data.get("procedure")
            else:
                procedure_name = ""

            if data.get("specialization"):
                specialization_name = data.get("specialization")
            else:
                specialization_name = ""

            if data.get("page"):
                page = data.get("page")
            else:
                page = 1

            if data.get("perpage"):
                limit = data.get("perpage")
            else:
                limit = str(settings.PAGE_SIZE)

            if data.get("hospital_array_id"):
                hospital_array_id = data.get("hospital_array_id")
                hospital_array_id = hospital_array_id.split(",")
            else:
                hospital_array_id = ""
            print(hospital_array_id)    

            if data.get("hospital_array_id"):
                hospital_array_id = data.get("hospital_array_id")
                hospital_array_id = hospital_array_id.split(",")
            else:
                hospital_array_id = ""

            if data.get("specialization_array_id"):
                specialization_array_id = data.get("specialization_array_id")
                specialization_array_id = specialization_array_id.split(",")
            else:
                specialization_array_id = ""  

            print(specialization_array_id)   

            if data.get("price1"):
                price1 = data.get("price1")
            else:
                price1 = ""

            if data.get("price2"):
                price2 = data.get("price2")
            else:
                price2 = ""

            if data.get("price3"):
                price3 = data.get("price3")
            else:
                price3 = ""   
            print(price3)    


    
            pages, skip = 1, 0

            sort_field = data.get("sort_field")

            sort_dir = data.get("sort_dir")

            if page and limit:
                page = int(page)
                limit = int(limit)
                skip = (page - 1) * limit    


            charge = Charge.objects.all()

            if procedure_name:
                charge=charge.filter(procedure__procedure_name=procedure_name)

            if insurance:
                charge = charge.filter(
                    Q(insurance__insurance_name=insurance)
                )

            if zip_code:
                charge=charge.filter(Q(hospital__zip_code=zip_code))   

            if specialization_name:
                charge=charge.filter(Q(hospital__specialization__name=specialization_name))  
            
            if hospital:
                charge=charge.filter(Q(hospital__hospital_name=hospital))

            if hospital_array_id:
                charge=charge.filter(Q(hospital__id__in=hospital_array_id))
                print(charge)

            if specialization_array_id:
                charge=charge.filter(Q(hospital__specialization__id__in=specialization_array_id))  
                print(charge)  
            if price1:
                charge=charge.filter(price__lte=100)

            if price2:
                charge=charge.filter(price__range=(100,500))      

            if price3:
                charge=charge.filter(price__gte=500)
                print(charge)        
 
            count = charge.count()

            if sort_field is not None and sort_dir is not None:
                if sort_dir == "asc":
                    if sort_field == "procedure":
                        charge = charge.order_by("procedure")
                    elif sort_field == "hospital":
                        charge = charge.order_by("hospital")
                    elif sort_field == "procedure_price":
                        charge = charge.order_by("procedure_price") 
                    elif sort_field == "cash_price":
                        charge = charge.order_by("-cash_price") 
                    elif sort_field == "unit_price":
                        charge = charge.order_by("-unit_price")                   
                    elif sort_field == "id":
                        charge = charge.order_by("id")

                    else:
                        charge = charge.order_by("id")
                elif sort_dir == "desc":
                    if sort_field == "procedure":
                        charge = charge.order_by("-procedure")
                    elif sort_field == "hospital":
                        charge = charge.order_by("-hospital")
                    elif sort_field == "procedure_price":
                        charge = charge.order_by("-procedure_price")        
                    elif sort_field == "cash_price":
                        charge = charge.order_by("-cash_price")     
                    elif sort_field == "unit_price":
                        charge = charge.order_by("-unit_price")          
                    elif sort_field == "id":
                        charge = charge.order_by("-id")

                    else:
                        charge = charge.order_by("-id")
            else:
                charge = charge.order_by("-id")

            if page and limit:
                charge = charge[skip : skip + limit]    
                pages = math.ceil(count / limit) if limit else 1
            if charge:
                charge = ChargeSerializer(charge, many=True).data

                return ResponseOk(
                    {
                        "data": charge,
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


class CreateCharge(APIView):
    """
    Create Charge
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Charge create API",
        operation_summary="Charge create API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "insurance": openapi.Schema(type=openapi.TYPE_INTEGER),
                "procedure": openapi.Schema(type=openapi.TYPE_INTEGER),
                "procedure_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "hospital": openapi.Schema(type=openapi.TYPE_INTEGER),
                "cash_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "unit_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "maximum_negotiated_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "minimum_negotiated_price": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    @csrf_exempt
    def post(self, request):
        serializer = CreateChargeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "Charge created succesfully",
                }
            )
        else:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Charge is not valid",
                }
            )



class GetCharge(APIView):
    """
    Get Charge by pk
    """
    
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.JWTAuthentication]

    csrf_exempt

    def get_object(self, pk):
        try:
            return Charge.objects.get(pk=pk)
        except Charge.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            charge = self.get_object(pk)
            serializer = ChargeSerializer(charge)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get Charge successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Charge Does Not Exist",
                }
            )




class UpdateCharge(APIView):
    """
    Update Charge
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Charge.objects.get(pk=pk)
        except Charge.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="Charge update API",
        operation_summary="Charge update API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "insurance": openapi.Schema(type=openapi.TYPE_INTEGER),
                "procedure": openapi.Schema(type=openapi.TYPE_INTEGER),
                "procedure_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "hospital": openapi.Schema(type=openapi.TYPE_INTEGER),
                "cash_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "unit_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "maximum_negotiated_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "minimum_negotiated_price": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            charge = self.get_object(pk)
            serializer = CreateChargeSerializer(charge, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "Charge updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Charge Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Charge Does Not Exist",
                }
            )



class DeleteCharge(APIView):
    """
    Delete Charge
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get_object(self, pk):
        try:
            return Charge.objects.get(pk=pk)
        except Charge.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            charge = self.get_object(pk)
            charge.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "charge deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "charge Does Not Exist",
                }
            )





class GetAllUserInsurance(APIView):
    """
    Get All UserInsurance
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get(self, request):

        try:
            user_insurance = UserInsurance.objects.all()

            serializer = UserInsuranceSerializer(user_insurance, many=True)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "UserInsurance list",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "UserInsurance Does Not Exist",
                }
            )


class CreateUserInsurance(APIView):
    """
    Create UserInsurance
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @swagger_auto_schema(
        operation_description="UserInsurance create API",
        operation_summary="UserInsurance create API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "insurance": openapi.Schema(type=openapi.TYPE_INTEGER),
                "group_number": openapi.Schema(type=openapi.TYPE_STRING ),
                "member_id": openapi.Schema(type=openapi.TYPE_STRING ),
            },
        ),
    )
    @csrf_exempt
    def post(self, request):
        serializer = CreateUserInsuranceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "UserInsurance created succesfully",
                }
            )
        else:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "UserInsurance is not valid",
                }
            )



class GetUserInsurance(APIView):
    """
    Get UserInsurance by pk
    """
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    csrf_exempt

    def get_object(self, pk):
        try:
            return UserInsurance.objects.get(pk=pk)
        except UserInsurance.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            user_insurance = self.get_object(pk)
            serializer = UserInsuranceSerializer(user_insurance)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get UserInsurance successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "UserInsurance Does Not Exist",
                }
            )




class UpdateUserInsurance(APIView):
    """
    Update UserInsurance
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return UserInsurance.objects.get(pk=pk)
        except UserInsurance.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="UserInsurance update API",
        operation_summary="UserInsurance update API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "insurance": openapi.Schema(type=openapi.TYPE_INTEGER),
                "group_number": openapi.Schema(type=openapi.TYPE_STRING ),
                "member_id": openapi.Schema(type=openapi.TYPE_STRING ),
            },
        ),
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            user_insurance = self.get_object(pk)
            serializer = CreateUserInsuranceSerializer(user_insurance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "UserInsurance updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "UserInsurance Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "UserInsurance Does Not Exist",
                }
            )



class DeleteUserInsurance(APIView):
    """
    Delete UserInsurance
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get_object(self, pk):
        try:
            return UserInsurance.objects.get(pk=pk)
        except UserInsurance.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            user_insurance = self.get_object(pk)
            user_insurance.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "UserInsurance deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "UserInsurance Does Not Exist",
                }
            )

