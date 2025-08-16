from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/auth/", include("users.urls")),
    path("api/recipes/", include("recipes.urls")),
    path("api/blogs/", include("blogs.urls")),
    path("api/contact/", include("contact.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)