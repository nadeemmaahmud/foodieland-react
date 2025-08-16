import email
import profile
from urllib import response
from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from foodieland.user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    ActivateSerializer,
    LoginSerializer,
    ProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
import requests 
from django.conf import settings
from google.oauth2 import id_token as id_token 
from google.auth.transport import requests as google_requests


User = get_user_model()




# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    

class ActivateView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ActivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Account activated successfully"}, status=status.HTTP_200_OK)
    

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({"detail": "Account not activated"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user" : ProfileSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class PassWordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]


class PassWordResetConfirmView(generics.CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user).data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        request.user.delete()
        return Response({"detail": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class GoogleLogInView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get('token')
        try:
            payload = google_id_token.verify_oauth2_token(token, google_requests.Request())
            email = payload["email"]
            name = payload.get("name", "")
        except Exception:
            return Response({"detail": "Invalid Google token"}, status=400)
        user, _ = User.objects.get_or_create(email=email, defaults={"name": name, "is_active": True})
        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh), "user": ProfileSerializer(user).data})
            


class FacebookLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        access_token = request.data.get("access_token")
        r = requests.get("https://graph.facebook.com/me", params={"fields": "id,name,email", "access_token": access_token})
        if r.status_code != 200:
            return Response({"detail": "Invalid Facebook token"}, status=400)
        data = r.json()
        email = data.get("email")
        if not email:
            return Response({"detail": "Email permission is required"}, status=400)
        user, _ = User.objects.get_or_create(email=email, defaults={"name": data.get("name", ""), "is_active": True})
        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh), "user": ProfileSerializer(user).data})

        




  











    







