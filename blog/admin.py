

# Register your models here.
from django.contrib import admin
from .models import BlogCategory, Blog

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_image']  # Add 'display_image' to list_display
    readonly_fields = ['display_image']  
    
    def display_image(self, obj):  
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return "No Image"
    display_image.allow_tags = True
    display_image.short_description = 'Image Preview'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'created_at'] 
    list_editable = ['is_published']
    list_filter = ['category', 'created_at', 'is_published'] 
    search_fields = ['title', 'content']