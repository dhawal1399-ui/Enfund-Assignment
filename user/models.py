# models.py
from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE,null=True)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE,null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f'{self.sender} -> {self.recipient}: {self.message}'
