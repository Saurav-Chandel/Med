from django.urls import path

from hospital import views

app_name = "hospital"

urlpatterns = [

    # Hospital
    path("api/v1/list/", views.GetAllHospital.as_view()),
    path("api/v1/create/", views.CreateHospital.as_view()),
    path("api/v1/get/<int:pk>/", views.GetHospital.as_view()),
    path("api/v1/update/<int:pk>/",views. UpdateHospital.as_view()),
    path("api/v1/delete/<int:pk>/", views.DeleteHospital.as_view()),


    # Specialization
    path("specialization/api/v1/list/", views.GetAllSpecialization.as_view()),
    path("specialization/api/v1/create/", views.CreateSpecialization.as_view()),
    path("specialization/api/v1/get/<int:pk>/", views.GetSpecialization.as_view()),
    path("specialization/api/v1/update/<int:pk>/",views. UpdateSpecialization.as_view()),
    path("specialization/api/v1/delete/<int:pk>/", views.DeleteSpecialization.as_view()),

]
