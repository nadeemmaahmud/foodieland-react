from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import os
from uuid import uuid4


User = get_user_model()


# Image upload path for category - unique name generate korar jonno
def category_image_upload_path(instance, filename):
    # Generate a unique filename to avoid conflicts
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('category_images', filename)

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(
        upload_to=category_image_upload_path, 
        null=True, 
        blank=True,
        help_text="Category display image"
    )
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    short_desc = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to="blog/images/", null=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title