from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Chat(models.Model):
    user = models.ManyToManyField(User)

    def __str__(self):
        result = []
        for cur_user in self.user.all():
            result.append(cur_user.username)
        return '.-'.join(result)

    def new(user1, user2):
        chat = Chat()
        chat.save()
        chat.user.add(user1, user2)
        return chat

    def get(username1, username2):
        user1 = User.objects.get(username=username1)
        user2 = User.objects.get(username=username2)
        chat_qs = Chat.objects.filter(user=user1).filter(user=user2)
        if not chat_qs:
            chat = Chat.new(user1, user2)
        else:
            chat = chat_qs[0]
        return chat


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sender.username}: {self.content}'

    def get_history(chat_id):
        return Message.objects.filter(chat=chat_id).order_by('timestamp')
