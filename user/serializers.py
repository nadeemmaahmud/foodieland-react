from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from django.conf import settings

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data, password=password)
        # send activation email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"{settings.FRONTEND_BASE_URL}/activate/{uid}/{token}"
        send_mail(
            subject="Verify your FoodieLand account",
            message=f"Click to activate your account: {activation_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user

class ActivateSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")
        try:
            uid_int = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid_int)
        except Exception:
            raise serializers.ValidationError("Invalid activation link")
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token")
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.is_active = True
        user.save(update_fields=["is_active"])
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "bio", "avatar", "date_joined"]
        read_only_fields = ["email", "date_joined", "id"]

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        email = self.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return  # do not leak existence
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f"{settings.FRONTEND_BASE_URL}/reset-password/{uid}/{token}"
        send_mail(
            subject="Reset your FoodieLand password",
            message=f"Reset here: {link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self, **kwargs):
        from django.utils.encoding import force_str
        uid = self.validated_data["uid"]
        token = self.validated_data["token"]
        new_password = self.validated_data["new_password"]
        uid_int = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid_int)
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token")
        user.set_password(new_password)
        user.save()
        return user