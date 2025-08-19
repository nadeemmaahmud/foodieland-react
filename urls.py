from django.urls import path
from .views import ContactMessageListCreate

urlpatterns = [
    path('messages/', ContactMessageListCreate.as_view(), name='contact-message-list'),
]
