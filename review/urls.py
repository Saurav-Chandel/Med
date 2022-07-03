from django.urls import path

from .views import *

app_name = "review"

urlpatterns = [
   
    # Review
    path("api/v1/list/", GetAllReview.as_view()),
    path("api/v1/create/", CreateReview.as_view()),
    path("api/v1/get/<int:pk>/", GetReview.as_view()),
    path("api/v1/update/<int:pk>/", UpdateReview.as_view()),
    path("api/v1/delete/<int:pk>/", DeleteReview.as_view()),
]