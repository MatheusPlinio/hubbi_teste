from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterUserView, UserDetailView, ChangePasswordView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("register/", RegisterUserView.as_view(), name="user_register"),
    path("me/", UserDetailView.as_view(), name="user_detail"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
