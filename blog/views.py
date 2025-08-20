from rest_framework import generics, permissions
from .models import Blog, BlogCategory
from .serializers import BlogSerializer, BlogCategorySerializer

class BlogListCreateView(generics.ListCreateAPIView):
    
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
    
        if self.request.user.is_authenticated:
            # Authenticated users see all blogs (including their own drafts)
            return Blog.objects.all().select_related('author', 'category')
        else:
            # Non-authenticated users only see published blogs
            return Blog.objects.filter(is_published=True).select_related('author', 'category')
    
    def perform_create(self, serializer):
        """
        Automatically set the author to the currently logged-in user
        """
        serializer.save(author=self.request.user)

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a blog to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of the blog
        return obj.author == request.user


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_queryset(self):
       
        if self.request.user.is_authenticated:
            # Authenticated users can access all blogs (including drafts)
            return Blog.objects.all().select_related('author', 'category')
        else:
            # Non-authenticated users can only access published blogs
            return Blog.objects.filter(is_published=True).select_related('author', 'category')


class BlogCategoryListView(generics.ListAPIView):
  
    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all()
    permission_classes = [permissions.AllowAny]