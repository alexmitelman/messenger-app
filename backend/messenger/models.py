from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content}'

    def get_history():
        return Message.objects.order_by('-timestamp').all()
