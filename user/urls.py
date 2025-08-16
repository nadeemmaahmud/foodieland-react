from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, ActivateView, LoginView, PassWordResetView, PassWordResetConfirmView,
    ProfileView, GoogleLogInView, FacebookLoginView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("activate/", ActivateView.as_view()),  # POST {uid, token}
    path("login/", LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("password/reset/", PassWordResetView.as_view()),
    path("password/reset/confirm/", PassWordResetConfirmView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("social/google/", GoogleLogInView.as_view()),
    path("social/facebook/", FacebookLoginView.as_view()),
]