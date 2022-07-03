from django.contrib import admin
from django.urls import path,include
# from user.models import *
from user import views

app_name = "user"

urlpatterns = [
    path("auth/api/v1/login/", views.LoginView.as_view(), name="login"),
    path("auth/api/v1/signup/", views.SignUpView.as_view(), name="signup"),
    path("auth/api/v1/logout/", views.LogoutView.as_view(), name="logout"),

    path(
        "auth/api/v1/forgot-password-email/",
        views.RequestPasswordResetEmailView.as_view(),
        name="forgot-password-email",
    ),
    path(
        "auth/api/v1/forgot-password/<uidb64>/<token>/",
        views.PasswordTokenCheckAPIView.as_view(),
        name="forgot-password-confirm",
    ),
    path(
        "auth/api/v1/forgot-password-complete/",
        views.SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
    path(
        "auth/api/v1/password-reset/",
        views.ResetPasswordAPIView.as_view(),
        name="password-reset",
    ),
    path(
        "auth/api/v1/update-profile/<int:pk>/",
        views.UpdateProfile.as_view(),
        name="password-reset",
    ),
    # Media
    path("media/api/v1/list/", views.GetAllMedia.as_view()),
    path("media/api/v1/create/", views.CreateMedia.as_view()),
    path("media/api/v1/get/<int:pk>/", views.GetMedia.as_view()),
    path("media/api/v1/update/<int:pk>/", views.UpdateMedia.as_view()),
    path("media/api/v1/delete/<int:pk>/", views.DeleteMedia.as_view()),
]


