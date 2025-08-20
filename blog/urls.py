from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
     
    path('', views.BlogListCreateView.as_view(), name='blog-list'),
    path('categories/', views.BlogCategoryListView.as_view(), name='category-list'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
]