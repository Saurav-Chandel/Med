from django.urls import path

from .views import *

app_name = "insurance"

urlpatterns = [

    # Insurance
    path("api/v1/list/", GetAllInsurance.as_view()),
    path("api/v1/create/", CreateInsurance.as_view()),
    path("api/v1/get/<int:pk>/", GetInsurance.as_view()),
    path("api/v1/update/<int:pk>/", UpdateInsurance.as_view()),
    path("api/v1/delete/<int:pk>/", DeleteInsurance.as_view()),
    # Procedure
    path("procedure/api/v1/list/", GetAllProcedure.as_view()),
    path("procedure/api/v1/create/", CreateProcedure.as_view()),
    path("procedure/api/v1/get/<int:pk>/", GetProcedure.as_view()),
    path("procedure/api/v1/update/<int:pk>/", UpdateProcedure.as_view()),
    path("procedure/api/v1/delete/<int:pk>/", DeleteProcedure.as_view()),
    # Charge
    path("charge/api/v1/list/", GetAllCharge.as_view()),
    path("charge/api/v1/create/", CreateCharge.as_view()),
    path("charge/api/v1/get/<int:pk>/", GetCharge.as_view()),
    path("charge/api/v1/update/<int:pk>/", UpdateCharge.as_view()),
    path("charge/api/v1/delete/<int:pk>/", DeleteCharge.as_view()),
    # User_Insurance
    path("user_insurance/api/v1/list/", GetAllUserInsurance.as_view()),
    path("user_insurance/api/v1/create/", CreateUserInsurance.as_view()),
    path("user_insurance/api/v1/get/<int:pk>/", GetUserInsurance.as_view()),
    path("user_insurance/api/v1/update/<int:pk>/", UpdateUserInsurance.as_view()),
    path("user_insurance/api/v1/delete/<int:pk>/", DeleteUserInsurance.as_view()),
]
