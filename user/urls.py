from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, ActivateView, LoginView, PasswordResetRequestView, PasswordResetConfirmView,
    ProfileView, GoogleLoginView, FacebookLoginView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("activate/", ActivateView.as_view()),  # POST {uid, token}
    path("login/", LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("password/reset/", PasswordResetRequestView.as_view()),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("social/google/", GoogleLoginView.as_view()),
    path("social/facebook/", FacebookLoginView.as_view()),
]