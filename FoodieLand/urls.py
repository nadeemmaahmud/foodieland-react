from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/auth/", include("user.urls")),
    #path("api/core/", include("core.urls")),
    #path("api/blogs/", include("blogs.urls")),
    #path("api/contact/", include("contact.urls")),
    path('api/blogs/', include('blog.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)