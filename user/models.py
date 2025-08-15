# from importlib.metadata import requires
# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#   email = models.EmailField(unique=True)
#   password = models.CharField(max_length=128)
#   first_name = models.CharField(max_length=30)
#   last_name = models.CharField(max_length=30)
#   bio = models.TextField(blank=True)
#   profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#   is_active = models.BooleanField(default=True)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

  



import profile
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_active = models.BooleanField(default=False)  # becomes True after email verify
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
