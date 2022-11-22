from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(unique=True, null=True, max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    def __str__(self):
        return f"{self.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField(max_length=1000, null=True)
    subject = models.CharField(max_length=50, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    read_date=models.DateTimeField(null=True)

    def __str__(self):
        return f"Sender: {self.sender} Subject: {self.subject} - Message: {self.message} - Date: {self.creation_date}"
