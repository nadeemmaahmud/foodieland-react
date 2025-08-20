from rest_framework import serializers
from .models import Blog, BlogCategory

class BlogCategorySerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField() 

    def get_image_url(self, obj):  # Add this method
        if obj.image:
            return obj.image.url
        return None
    
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'image', 'image_url']

class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'short_desc', 'image', 
            'content', 'author', 'author_name',
            'category', 'category_name', 'created_at', 
            'updated_at', 'is_published' 
        ]
        extra_kwargs = {
            'author': {'read_only': True}
        }