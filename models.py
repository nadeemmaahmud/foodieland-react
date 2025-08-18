from django.conf import settings
from django.db import models

class ContactMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="messages"
    )  
    name = models.CharField(max_length=200)
    email = models.EmailField(default="example@example.com")

    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)  # timestamp when message is sent
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message from {self.name} ({self.email}) at {self.sent_at}"
