from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.username}'


class Chat(models.Model):
    first_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    second_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id chat: {self.pk} users: {self.first_user} - {self.second_user}'

    class Meta:
        verbose_name = 'chat'
        app_label = 'logic'


class Message(models.Model):
    text = models.CharField(max_length=255, blank=False)
    id_chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    id_sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    id_recipient = models.ForeignKey(to=User, on_delete=models.CASCADE)
    ip_sender = models.GenericIPAddressField(max_length=15)
    time_send_message = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'message'
        app_label = 'logic'
